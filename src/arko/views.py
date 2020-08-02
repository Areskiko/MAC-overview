from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from django import forms
from .models import Device
from .forms import DeviceForm
from netScan import scan, lookup, update
from datetime import datetime
import threading


def strfdelta(tdelta):
    d = {"days": tdelta.days}
    d["hours"], rem = divmod(tdelta.seconds, 3600)
    d["minutes"], d["seconds"] = divmod(rem, 60)
    return d

def updateDevices():
    while True:
        today = timezone.now()

        #Update devices database
        devices = Device.objects.all()
        devicesMac = [device.mac for device in devices]
        devicesIp = [device.ip for device in devices]
        presentDevicesMacs, allMacs, allIps = update(devicesMac, devicesIp)
        for device in devices:
            if device.mac in presentDevicesMacs:
                device.ip = allIps[allMacs.index(device.mac)]
                device.seenAgo = "Online"
                device.lastSeen = today
                device.save()
            else:
                delta = today-device.lastSeen
                diff = strfdelta(delta)
                device.seenAgo = f"""Last seen \
                    {diff['days'] if (diff['days'] > 0) else ''} {'days' if (diff['days'] > 1) else f"{ 'day' if (diff['days'] > 0) else ''}" } \
                    {diff['hours'] if (diff['days'] < 1 and diff["hours"] > 0) else ''} {'hours' if (diff['days'] < 1 and diff['hours'] > 1) else f"{ 'hour' if (diff['hours'] > 0 and diff['days'] < 1) else ''}" } \
                    {diff['minutes'] if diff['hours'] < 1 else ''} {'minutes' if (diff['hours'] < 1 and diff['minutes'] > 1) else f"{ 'minute' if (diff['minutes'] > 0 and diff['hours'] < 1) else ''}" } \
                    ago"""
                device.save()

updateThread = threading.Thread(target=updateDevices, daemon=True)
updateThread.start()

# Create your views here.

unknownDevices = lookup(scan())


def Home(request):
    return render(request, "Arko/home.html", {"title":"Net Scanner"})

def Scanner(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = DeviceForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            form.save()
            name = form.cleaned_data["name"]
            messages.success(request, f"Now tracking {name}!")
            return redirect("Arko-scanner")
    context = {
        "title" : "Net Scanner",
        }
    return render(request, "Arko/scanner.html", context)

def Tracked(request):
    today = timezone.now()
    #Update devices list
    devices = Device.objects.all()
    #Get forms with values (instance)
    deviceForms = []
    for device in devices:
        form = DeviceForm(instance=device)
        form.fields["name"].widget = forms.HiddenInput()
        form.fields["mac"].widget = forms.HiddenInput()
        form.fields["ip"].widget = forms.HiddenInput()
        deviceForms.append(form)
    #Zip together to itterate through together in template
    zipped = [[device, form] for device, form in zip(devices, deviceForms)]

    return render(request, "Arko/tracked.html", {"title":"Net Scanner", "zipped": zipped, "today":today})

def Untracked(request):
    
    devices = Device.objects.all()
    devicesMac = [device.mac for device in devices]
    unknownDevices = lookup(scan())
    unknownDevices = [device for device in unknownDevices if device[0] not in devicesMac]

    unknownForms = []
    for unknownDevice in unknownDevices:
        form = DeviceForm(initial={"mac":unknownDevice[0], "ip":unknownDevice[1]})
        form.fields["mac"].widget = forms.HiddenInput()
        form.fields["ip"].widget = forms.HiddenInput()
        form.fields["name"].widget.attrs['class'] = 'scale-transition scale-out'
        unknownForms.append(form)
    zipped = [[unknown, form] for unknown, form in zip(unknownDevices, unknownForms)]
    return render(request, "Arko/untracked.html", {"title":"Net Scanner", "zipped":zipped})


def RemoveTrack(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = DeviceForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            name = form.cleaned_data["name"]
            mac = form.cleaned_data["mac"]
            Device.objects.get(mac=mac).delete()
            messages.success(request, f"No longer tracking {name}!")
            return redirect("Arko-scanner")
        else:
            return render(request, "Arko/error.html")

