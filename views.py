from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from artapp.models import CustomUser,Artist,Arttype,Artmedium,Artproducts,Page,Enquiry
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import random
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
User = get_user_model()


def BASE(request):    
       return render(request,'base.html')


def BASE1(request):    
    return render(request,'base1.html')

def Header(request):
    arttypes = Arttype.objects.all() 
    return render(request,'includes1/header.html', {'arttypes': arttypes})


def Index(request):
    artproducts1 = Artproducts.objects.all()
     
    context = {
        
        "artproducts1":artproducts1,
      
    }
    return render(request,'index.html',context)

def ABOUTUS(request):
    first_page = Page.objects.first()
    context = {
        "page": first_page,
    }
    return render(request, 'aboutus.html', context)

def CONTACTUS(request):
    first_page = Page.objects.first()
    context = {
        "page": first_page,
    }
    return render(request, 'contactus.html', context)



def VIEW_SINGLEPRODUCTS(request,id):    
    sinprod = Artproducts.objects.get(id =id)
     
    context = {
        
        "sinprod":sinprod,
      
    }
    return render(request,'single-artproduct-details.html',context)

def arttype_detail(request, id):
    arttype_id = get_object_or_404(Arttype, id=id)
    artproducts = Artproducts.objects.filter(arttype=arttype_id)  # Using the related_name 'artproducts'
    return render(request, 'arttype_prodetail.html', {'arttype_id': arttype_id, 'artproducts': artproducts})

def ENQUIRY(request,id):    
    sinprod = Artproducts.objects.get(id =id)
     
    context = {
        
        "sinprod":sinprod,
      
    }
    return render(request,'enquiry.html',context)


def ENQUIRY_DETAILS(request):
    if request.method == "POST":
        try:
            # Retrieve the Artproducts instance using the provided prod_id
            prod_id = request.POST['prod_id']
            art_product = Artproducts.objects.get(pk=prod_id)

            # Create the Enquiry object with the Artproducts instance
            enquirynumber = random.randint(100000000, 999999999)
            enq_obj = Enquiry(
                enquirynumber=enquirynumber,
                fullname=request.POST['fullname'],
                prod_id=art_product,
                email=request.POST['email'],
                mobnum=request.POST['mobnum'],
                message=request.POST['message'],
            )
            enq_obj.save()           
            return redirect('thank_you', enquirynumber=enquirynumber)
        except Artproducts.DoesNotExist:
            messages.error(request, "The selected product does not exist")
        except IntegrityError:
            messages.error(request, "Email and Mobile number must be unique")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
    
    return render(request, 'enquiry.html')

def THANKYOU(request, enquirynumber):
    context = {
        "enquirynumber": enquirynumber,
    }
    return render(request, 'thankyou.html', context)


def ARTPRODUCTLIST(request):    
    artproduct_list = Artproducts.objects.all()
    paginator = Paginator(artproduct_list, 9)  # Show 10 categories per page

    page_number = request.GET.get('page')
    try:
       artproducts = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        artproducts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        artproducts = paginator.page(paginator.num_pages)

    context = {
    'artproducts':artproducts,}
    return render(request, 'artproducts-list.html', context)

def LOGIN(request):
    return render(request,'login.html')

def doLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
       

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            user_type = user.user_type
            if user_type == '1':
                return redirect('dashboard')
            elif user_type == '2':
                return redirect('dashboard')
        else:
            messages.error(request, 'Email or Password is not valid')
            return redirect('login')  # Redirect back to the login page with an error message
    else:
        # If the request method is not POST, redirect to the login page with an error message
        messages.error(request, 'Invalid request method')
        return redirect('login')

def doLogout(request):
    logout(request)
    request.session.flush()  # Clear the session including CSRF token
    return redirect('login')

@login_required(login_url = '/')
def DASHBOARD(request):
    artist_count = Artist.objects.all().count
    type_count = Arttype.objects.all().count
    med_count = Artmedium.objects.all().count
    artprod_count = Artproducts.objects.all().count
    unreadenq_count = Enquiry.objects.filter(status='').count()
    readenq_count = Enquiry.objects.filter(status='Answered').count()
    context = {'artist_count':artist_count,
    'type_count': type_count,
    'med_count':med_count,
    'artprod_count':artprod_count,
    'unreadenq_count':unreadenq_count,
    'readenq_count':readenq_count,
         
    }       
    return render(request,'dashboard.html',context)



@login_required(login_url = '/')
def ADMIN_PROFILE(request):
    user = CustomUser.objects.get(id = request.user.id)
    context = {
        "user":user,
    }
    return render(request,'profile.html',context)


@login_required(login_url = '/')
def ADMIN_PROFILE_UPDATE(request):
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        print(profile_pic)
        

        try:
            customuser = CustomUser.objects.get(id = request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            

            
            if profile_pic !=None and profile_pic != "":
               customuser.profile_pic = profile_pic
            customuser.save()
            messages.success(request,"Your profile has been updated successfully")
            return redirect('admin_profile')

        except:
            messages.error(request,"Your profile updation has been failed")
    return render(request, 'profile.html')


login_required(login_url='/')
def CHANGE_PASSWORD(request):
     context ={}
     ch = User.objects.filter(id = request.user.id)
     
     if len(ch)>0:
            data = User.objects.get(id = request.user.id)
            context["data"]:data            
     if request.method == "POST":        
        current = request.POST["cpwd"]
        new_pas = request.POST['npwd']
        user = User.objects.get(id = request.user.id)
        un = user.username
        check = user.check_password(current)
        if check == True:
          user.set_password(new_pas)
          user.save()
          messages.success(request,'Password Change  Succeesfully!!!')
          user = User.objects.get(username=un)
          login(request,user)
        else:
          messages.success(request,'Current Password wrong!!!')
          return redirect("change_password")
     return render(request,'change-password.html')



@login_required(login_url = '/')
def ADD_ARTIST(request):
    if request.method == "POST":
        try:
            artist_obj = Artist(
                name=request.POST['name'],
                mobnum=request.POST['mobnum'],
                email=request.POST['email'],
                edudetails=request.POST['edudetails'],
                awarddetails=request.POST['awarddetails'],
                
                images = request.FILES.get('images')
                
            )
            artist_obj.save()
            messages.success(request, "Artist details has been created successfully")
            return redirect('add_artist')
        except IntegrityError:
            messages.error(request, "Email and Mobilenumber must be unique")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
    
    return render(request,'add-artist.html')


@login_required(login_url='/')
def MANAGE_ARTIST(request):    
    artist_list = Artist.objects.all()
    paginator = Paginator(artist_list, 10)  # Show 10 categories per page

    page_number = request.GET.get('page')
    try:
        artists = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        artists = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        artists = paginator.page(paginator.num_pages)

    context = {
    'artists':artists,}
    return render(request, 'manage-artist.html', context)

@login_required(login_url='/')
def DELETE_ARTIST(request,id):
    art = Artist.objects.get(id=id)
    art.delete()
    messages.success(request,'Record Delete Succeesfully!!!')
    
    return redirect('manage_artist')


@login_required(login_url='/')
def VIEW_ARTIST(request,id):    
    artist_data = Artist.objects.get(id =id)    
    context = {
        
        "artist_data":artist_data,
    }
    return render(request,'update_artist.html',context)

@login_required(login_url='/')
def EDIT_ARTIST(request):
    if request.method == "POST":
        artist_id = request.POST.get('artist_id')
        try:
            artist_edit = Artist.objects.get(id=artist_id)
        except Notes.DoesNotExist:
            messages.error(request, "Artist details does not exist")
            return redirect('manage_artist')

        # Create a dictionary with updated data
        updated_artist = {
            
            'name': request.POST['name'],
            'mobnum': request.POST['mobnum'],
            'email': request.POST['email'],
            'edudetails': request.POST['edudetails'],
            'awarddetails': request.POST['awarddetails'],
            'images': request.FILES.get('images')
        }

        # Update the artist_edit object with the updated artist
        for field, value in updated_artist.items():
            if value:
                setattr(artist_edit, field, value)

        
        artist_edit.save()
        messages.success(request, "Artist details has been updated successfully")
        return redirect('manage_artist')

    return render(request, 'manage-artist.html')

@login_required(login_url='/')
def ADD_ARTTYPE(request):
    if request.method == "POST":
        arttype_value = request.POST.get('arttype')
        if arttype_value:
            try:
                type_obj = Arttype(arttype=arttype_value)
                type_obj.save()
                messages.success(request, "Art type has been created successfully")
                return redirect('add_arttype')
            except IntegrityError:
                messages.error(request, "This art type already exists.")
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")
        else:
            messages.error(request, "Please provide a valid art type.")
    
    return render(request, 'add-arttype.html')


@login_required(login_url='/')
def ADD_ARTMEDIUM(request):
    if request.method == "POST":
        artmedium_value = request.POST.get('artmedium')
        if artmedium_value:
            try:
                medium_obj = Artmedium(artmedium=artmedium_value)
                medium_obj.save()
                messages.success(request, "Art medium has been created successfully")
                return redirect('add_artmedium')
            except IntegrityError:
                messages.error(request, "This art medium already exists.")
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")
        else:
            messages.error(request, "Please provide a valid art type.")
    
    return render(request, 'add-artmedium.html')


@login_required(login_url='/')
def MANAGE_ARTTYPE(request):    
    type_list = Arttype.objects.all()
    paginator = Paginator(type_list, 10)  # Show 10 categories per page

    page_number = request.GET.get('page')
    try:
        arttype = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        arttype = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        arttype = paginator.page(paginator.num_pages)

    context = {
    'arttype':arttype,}
    return render(request, 'manage-arttype.html', context)

@login_required(login_url='/')
def DELETE_ARTTYPE(request,id):
    arttype = Arttype.objects.get(id=id)
    arttype.delete()
    messages.success(request,'Record Delete Succeesfully!!!')
    
    return redirect('manage_arttype')


@login_required(login_url='/')
def MANAGE_ARTMEDIUM(request):    
    medium_list = Artmedium.objects.all()
    paginator = Paginator(medium_list, 10)  # Show 10 categories per page

    page_number = request.GET.get('page')
    try:
        medium = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        medium = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        medium = paginator.page(paginator.num_pages)

    context = {
    'medium':medium,}
    return render(request, 'manage-artmedium.html', context)

@login_required(login_url='/')
def DELETE_ARTMEDIUM(request,id):
    artmed = Artmedium.objects.get(id=id)
    artmed.delete()
    messages.success(request,'Record Delete Succeesfully!!!')
    
    return redirect('manage_artmedium')


@login_required(login_url='/')
def add_artproduct(request):
    if request.method == "POST":
        try:
            referencenumber = random.randint(100000000, 999999999)
            title = request.POST.get('title')
            images = request.FILES.get('images')
            image1 = request.FILES.get('image1')
            image2 = request.FILES.get('image2')
            image3 = request.FILES.get('image3')
            image4 = request.FILES.get('image4')
            dimension = request.POST.get('dimension')
            orientation = request.POST.get('orientation')
            size = request.POST.get('size')
            artist_id = request.POST.get('artist')
            arttype_id = request.POST.get('arttype')
            artmedium_id = request.POST.get('artmedium')
            sellingprice = request.POST.get('sellingprice')
            description = request.POST.get('description')

            artist = Artist.objects.get(id=artist_id) if artist_id else None
            arttype = Arttype.objects.get(id=arttype_id) if arttype_id else None
            artmedium = Artmedium.objects.get(id=artmedium_id) if artmedium_id else None

            artproduct = Artproducts(
                referencenumber=referencenumber,
                title=title,
                images=images,
                image1=image1,
                image2=image2,
                image3=image3,
                image4=image4,
                dimension=dimension,
                orientation=orientation,
                size=size,
                artist=artist,
                arttype=arttype,
                artmedium=artmedium,
                sellingprice=sellingprice,
                description=description,
            )
            artproduct.save()
            messages.success(request, "Art product has been created successfully")
            return redirect('add_artproduct')
        except IntegrityError:
            messages.error(request, "A product with this reference number already exists.")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")

    artists = Artist.objects.all()
    arttypes = Arttype.objects.all()
    artmediums = Artmedium.objects.all()
    return render(request, 'add-artproduct.html', {
        'artists': artists,
        'arttypes': arttypes,
        'artmediums': artmediums,
    })


@login_required(login_url='/')
def MANAGE_ARTPRODUCTS(request):    
    product_list = Artproducts.objects.all()
    paginator = Paginator(product_list, 10)  # Show 10 categories per page

    page_number = request.GET.get('page')
    try:
       products = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        products = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        products = paginator.page(paginator.num_pages)

    context = {
    'products':products,}
    return render(request, 'manage-artproducts.html', context)

@login_required(login_url='/')
def DELETE_ARTPRODUCT(request,id):
    artpro = Artproducts.objects.get(id=id)
    artpro.delete()
    messages.success(request,'Record Delete Succeesfully!!!')
    
    return redirect('manage_artproduct')

@login_required(login_url='/')
def VIEW_ARTPRODUCTS(request,id):    
    prod = Artproducts.objects.get(id =id)
    artists = Artist.objects.all()
    arttypes = Arttype.objects.all()
    artmediums = Artmedium.objects.all()    
    context = {
        
        "prod":prod,
        "artists":artists,
        "arttypes":arttypes,
        "artmediums":artmediums,
    }
    return render(request,'update_artproducts.html',context)

@login_required(login_url='/')
def VIEW_PRODUCTS(request, prod_id):    
    prod = get_object_or_404(Artproducts, id=prod_id)
    artists = Artist.objects.all()
    arttypes = Arttype.objects.all()
    artmediums = Artmedium.objects.all()    

    context = {
        "prod": prod,
        "artists": artists,
        "arttypes": arttypes,
        "artmediums": artmediums,
    }
    return render(request, 'update_artproducts.html', context)

@login_required(login_url='/')
def EDIT_ARTPRODUCTS(request):
    if request.method == "POST":
        pro_id = request.POST.get('pro_id')
        try:
            prod_edit = Artproducts.objects.get(id=pro_id)
        except Artproducts.DoesNotExist:
            messages.error(request, "Data does not exist")
            return redirect('manage_artproduct')

        # Create a dictionary with updated data
        updated_prod = {
            'title': request.POST.get('title'),
            'dimension': request.POST.get('dimension'),
            'orientation': request.POST.get('orientation'),
            'size': request.POST.get('size'),
            'sellingprice': request.POST.get('sellingprice'),
            'description': request.POST.get('description'),
        }

        # Update the prod_edit object with the updated data
        for field, value in updated_prod.items():
            if value:
                setattr(prod_edit, field, value)

        # Handle foreign key fields separately
        try:
            artist_id = request.POST.get('artist')
            if artist_id:
                prod_edit.artist = Artist.objects.get(id=artist_id)
            arttype_id = request.POST.get('arttype')
            if arttype_id:
                prod_edit.arttype = Arttype.objects.get(id=arttype_id)
            artmedium_id = request.POST.get('artmedium')
            if artmedium_id:
                prod_edit.artmedium = Artmedium.objects.get(id=artmedium_id)
        except (Artist.DoesNotExist, Arttype.DoesNotExist, Artmedium.DoesNotExist) as e:
            messages.error(request, f"Related entity error: {str(e)}")
            return redirect('manage_artproduct')

        # Handle file uploads separately
        image_fields = ['images', 'image1', 'image2', 'image3', 'image4']
        for image_field in image_fields:
            if image_field in request.FILES:
                setattr(prod_edit, image_field, request.FILES[image_field])

        prod_edit.save()
        messages.success(request, "Data has been updated successfully")
        return redirect('manage_artproduct')

    return render(request, 'manage-artproducts.html')


@login_required(login_url='/')
def WEBSITE_UPDATE(request):
    if request.method == "POST":
        try:
            web_id = request.POST.get('web_id')
            page = Page.objects.get(id=web_id)
            page.pagetitle = request.POST.get('pagetitle')
            page.address = request.POST.get('address')
            page.aboutus = request.POST.get('aboutus')
            page.mobilenumber = request.POST.get('mobilenumber')
            page.email = request.POST.get('email')
            page.save()
            messages.success(request, "Page has been updated successfully")
            return redirect('website_update')
        except Page.DoesNotExist:
            messages.error(request, "Page does not exist")
            return redirect('website_update')
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('website_update')
    
    pages = Page.objects.all()
    context = {
        "pages": pages,
    }
    return render(request, 'website.html', context)


@login_required(login_url='/')
def TOTALENQUIRY(request):    
    total_enq = Enquiry.objects.all()
    paginator = Paginator(total_enq, 10)  # Show 10 enquiries per page

    page_number = request.GET.get('page')
    try:
        tot_enq = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        tot_enq = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        tot_enq = paginator.page(paginator.num_pages)

    context = {
        'tot_enq': tot_enq,
    }
    return render(request, 'total_enquiry.html', context)


@login_required(login_url='/')
def UNANSWERED_ENQUIRY(request):    
    unanswered_enq = Enquiry.objects.filter(status='')
    paginator = Paginator(unanswered_enq, 10)  # Show 10 enquiries per page

    page_number = request.GET.get('page')
    try:
        unanswered_enq = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        unanswered_enq = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        unanswered_enq = paginator.page(paginator.num_pages)

    context = {
        'unanswered_enq': unanswered_enq,
    }
    return render(request, 'unanswered-enquiry.html', context)

@login_required(login_url='/')
def ANSWERED_ENQUIRY(request):    
    answered_enq = Enquiry.objects.filter(status='Answered')
    paginator = Paginator(answered_enq, 10)  # Show 10 enquiries per page

    page_number = request.GET.get('page')
    try:
        answered_enq = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        answered_enq = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        answered_enq = paginator.page(paginator.num_pages)

    context = {
        'answered_enq': answered_enq,
    }
    return render(request, 'answered-enquiry.html', context)

@login_required(login_url='/')
def VIEW_ENQUIRY(request,id):    
    view_enq = Enquiry.objects.filter(id=id)
      
    context = {
         'view_enq':view_enq,
         
    }
    return render(request,'view-enquiry-details.html',context)


def UPDATE_ENQUIRY_REMARK(request):
    enq_id = request.POST.get('enq_id')
    remark_text = request.POST.get('remark')

    try:
        enquiry_update = Enquiry.objects.get(id=enq_id)
        enquiry_update.remark = remark_text
        enquiry_update.status = 'Answered'
        enquiry_update.remark_date = timezone.now()  # Assuming there's a field to record the date of the remark
        enquiry_update.save()

        messages.success(request, "Status updated successfully")
    except Enquiry.DoesNotExist:
        messages.error(request, "Enquiry not found")
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")

    return redirect('totalenquiry')


def SEARCH_ENQUIRY(request):
    if request.method == "GET":
        query = request.GET.get('query', '')
        if query:
            # Filter records where email or mobilenumber contains the query
            searchenq = Enquiry.objects.filter(enquirynumber__icontains=query) | Enquiry.objects.filter(mobnum__icontains=query) | Enquiry.objects.filter(fullname__icontains=query)
            messages.info(request, "Search against " + query)
            return render(request, 'search-enquiry.html', {'searchenq': searchenq, 'query': query})
        else:
            print("No Record Found")
            return render(request, 'search-enquiry.html', {})

