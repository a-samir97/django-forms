from django.shortcuts import render
from .forms import PizzaForm, MultiplePizzaForm
from django.forms import formset_factory
from .models import Pizza

def home(request):
    return render(request,'home.html')

def order(request):

    multiple_pizza_form = MultiplePizzaForm()
    if  request.method == 'POST':
        filled_form = PizzaForm(request.POST)
        if filled_form.is_valid():
            pizza_id = filled_form.save().id
            note = "Thanks for ordering ! Your {} {} and {} Pizza in its way, Please wait".format(
                filled_form.cleaned_data['size'],
                filled_form.cleaned_data['topping1'],
                filled_form.cleaned_data['topping2']
            )
            new_pizza_form = PizzaForm()
            return render(request, 'order.html',{
                                                'form':new_pizza_form,
                                                'note':note,
                                                'multiple_pizzas':multiple_pizza_form,
                                                'pizza_id':pizza_id})
        else:
            note = "Please there is something wrong, please try again"
            new_pizza_form = PizzaForm()
            return render(request,'order.html',{
                                                'form':new_pizza_form,
                                                'note':note,
                                                'multiple_pizzas':multiple_pizza_form})
    else:
        pizza_form = PizzaForm()
        return render(request, 'order.html', {'form':pizza_form,'multiple_pizzas':multiple_pizza_form})

def multiple_pizza(request):
    # initial value
    number_of_pizzas = 2
    # get number of pizzas selected by user
    filled_multiple_pizza_form = MultiplePizzaForm(request.GET)
    # check if the form is valid
    if filled_multiple_pizza_form.is_valid():
        # update number of pizzas variable
        number_of_pizzas = filled_multiple_pizza_form.cleaned_data['number']
    # create formset with the selected number_of_pizzas
    PizzaFormSet = formset_factory(PizzaForm,extra=number_of_pizzas)
    # this is the new formset
    formset = PizzaFormSet()
    # check of the method is POST method
    if request.method == 'POST':
        # get the request.POST data
        filled_formset = PizzaFormSet(request.POST)
        # if formset is valid
        if filled_formset.is_valid():
            # looping for all formsets
            for form in filled_formset:
                # print topping1 to check if the formset is good :D
                print(form.cleaned_data['topping1'])
            # note that will appear to the user
            note = 'Pizzas are Ordered :D'
        # if the formset is not valid
        else:
            note ='Order was not created, Please try again'

        return render(request,'pizzas.html',{'formset':formset,'note':note})

    # if method is GET method
    else:
        return render(request,'pizzas.html',{'formset':formset})



def edit_order(request,pk):
    pizza = Pizza.objects.filter(pk=pk).first()
    form = PizzaForm(instance=pizza)

    if request.method == 'POST':
        filled_form = PizzaForm(request.POST, instance=pizza)
        if filled_form.is_valid():
            filled_form.save()
            note = 'Your Order is Updated !!'
        else:
            note = 'Please Try again , there is something goes wrong'
        return render(request,'edit-order.html',{'form':filled_form,'pizza_id':pk, 'note':note})
    else:
        return render(request,'edit-order.html',{'form':form})
