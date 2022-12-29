from django.shortcuts import redirect
from django.views.generic.base import View
from . models import Movie, Category, Actor, Genre, Rating
from .forms import ReviewForm
from django.db.models import Q
from django.views.generic import ListView, DetailView
from .forms import RatingForm


class GenreYear:
    def get_genres(self):
        return Genre.objects.all()

    def get_years(self):
        return Movie.objects.filter(draft=False).values('year')


class MovieView(GenreYear, ListView):
    model = Movie 
    queryset = Movie.objects.filter(draft=False)
    # template_name = 'movies/movies.html'
    



class MovieDetailView(GenreYear, DetailView):
    model = Movie 
    slug_field = 'url'
    

    def get_context_data(self, **kwagrs):
        context = super().get_context_data(**kwagrs)
        context['star_form'] = RatingForm()
        return context

class AddReview(View):
   def post(self, request, pk):
        form = ReviewForm(request.POST)
        movie = Movie.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get("parent", None):
                form.parent_id = int(request.POST.get("parent"))
            form.movie = movie
            form.save()
        return redirect(movie.get_absolute_url())    
    
class FilterMoviesView(GenreYear, ListView):
    def get_queryset(self):
        queryset = Movie.objects.filter(
            Q(year__in=self.request.GET.getlist('year')) |
            Q(genres__in=self.request.GET.getlist('genre'))
        )
        return queryset


class Search(ListView):

    paginate_by = 3


    def get_queryset(self):
        return Movie.objects.filter(title__icontains=self.request.GET.get("q"))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = self.request.GET.get("q")
        return context

