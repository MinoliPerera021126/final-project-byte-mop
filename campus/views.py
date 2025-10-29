from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required  # use if you want to require login
from .models import Zone, Building, Division, Task
from .forms import ZoneForm, BuildingForm, DivisionForm, TaskForm, SubtaskFormSet
from .models import Building

# ---------- HOME ----------
def home(request):
    return render(request, 'campus/home.html')

# ---------- ZONES: list/create/edit/delete ----------
def zone_list_create(request):
    zones = Zone.objects.all().order_by('name')
    if request.method == 'POST':
        form = ZoneForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Zone created.")
            return redirect('campus:zone_list')
    else:
        form = ZoneForm()

    
    zones = Zone.objects.all().prefetch_related('buildings__divisions')

    context = {
        'form': form,
        'zones': zones,
    }
    return render(request, 'campus/zone_list_create.html', context)

def zone_edit(request, pk):
    zone = get_object_or_404(Zone, pk=pk)
    if request.method == 'POST':
        form = ZoneForm(request.POST, instance=zone)
        if form.is_valid():
            form.save()
            messages.success(request, "Zone updated.")
            return redirect('campus:zone_list')
    else:
        form = ZoneForm(instance=zone)
    return render(request, 'campus/zone_edit.html', {'form': form, 'zone': zone})

def zone_delete(request, pk):
    zone = get_object_or_404(Zone, pk=pk)
    if request.method == 'POST':
        zone.delete()
        messages.success(request, "Zone deleted.")
        return redirect('campus:zone_list')
    return render(request, 'campus/confirm_delete.html', {'obj': zone, 'cancel_url': reverse('campus:zone_list')})

# ---------- BUILDINGS: list/create/edit/delete ----------
def building_list_create(request):
    from .models import Zone
    zones = Zone.objects.all()
    if not zones.exists():
        messages.warning(request, "No zones exist. Create a zone first.")
        return render(request, 'campus/need_zone.html')

    buildings = Building.objects.select_related('zone').all().order_by('zone__name', 'name')
    if request.method == 'POST':
        form = BuildingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Building created.")
            return redirect('campus:building_list')
    else:
        form = BuildingForm()
    return render(request, 'campus/building_list_create.html', {'buildings': buildings, 'form': form})

def building_edit(request, pk):
    building = get_object_or_404(Building, pk=pk)
    if request.method == 'POST':
        form = BuildingForm(request.POST, instance=building)
        if form.is_valid():
            form.save()
            messages.success(request, "Building updated.")
            return redirect('campus:building_list')
    else:
        form = BuildingForm(instance=building)
    return render(request, 'campus/building_edit.html', {'form': form, 'building': building})

def building_delete(request, pk):
    building = get_object_or_404(Building, pk=pk)
    if request.method == 'POST':
        building.delete()
        messages.success(request, "Building deleted.")
        return redirect('campus:building_list')
    return render(request, 'campus/confirm_delete.html', {'obj': building, 'cancel_url': reverse('campus:building_list')})

# ---------- DIVISIONS: list/create/edit/delete (with assistant assignment) ----------
def division_list_create(request):
    from .models import Building
    buildings = Building.objects.all()
    if not buildings.exists():
        messages.warning(request, "No buildings exist. Create a building first.")
        return render(request, 'campus/need_building.html')

    divisions = Division.objects.select_related('building__zone', 'assistant').all().order_by('building__name', 'name')
    if request.method == 'POST':
        form = DivisionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Division created.")
            return redirect('campus:division_list')
    else:
        form = DivisionForm()

    buildings = Building.objects.all().prefetch_related('divisions')

    # If you don’t have related_name='divisions' in your model, use:
    # buildings = Building.objects.all().prefetch_related('division_set')

    return render(request, 'campus/division_list_create.html', {
        'form': form,
        'buildings': buildings
    })
    #return render(request, 'campus/division_list_create.html', {'divisions': divisions, 'form': form})

def division_edit(request, pk):
    division = get_object_or_404(Division, pk=pk)
    if request.method == 'POST':
        form = DivisionForm(request.POST, instance=division)
        if form.is_valid():
            form.save()
            messages.success(request, "Division updated.")
            return redirect('campus:division_list')
    else:
        form = DivisionForm(instance=division)
    return render(request, 'campus/division_edit.html', {'form': form, 'division': division})

def division_delete(request, pk):
    division = get_object_or_404(Division, pk=pk)
    if request.method == 'POST':
        division.delete()
        messages.success(request, "Division deleted.")
        return redirect('campus:division_list')
    return render(request, 'campus/confirm_delete.html', {'obj': division, 'cancel_url': reverse('campus:division_list')})


