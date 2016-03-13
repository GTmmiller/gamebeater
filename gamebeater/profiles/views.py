from django.shortcuts import render, get_object_or_404
from django.views.generic import View, UpdateView, CreateView, ListView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.http import Http404

from .forms import UserForm, CompletionStatusUpdateForm, GameOwnershipForm, GameOwnershipUpdateForm, GoalStatusUpdateForm, GoalCreationForm, GoalCompletionStatusUpdateForm
from .models import GamebeaterProfile, GameOwnership, Goal
from .statuses import get_all_objects_by_status, CompletionStatus

class DashboardView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        # TODO: add default values to forms
        # Handles display of Gamebeater Profile
        profile_pk = request.user.gamebeaterprofile.pk
        gamebeaterprofile = get_object_or_404(GamebeaterProfile, pk=profile_pk)
        gameownerships_by_completion_status_list = get_all_objects_by_status(gamebeaterprofile.games, CompletionStatus, gamebeaterprofile.get_gameownerships_by_completion)
        return render(
            request,
            'profiles/dashboard.html',
            {
                "gamebeaterprofile": gamebeaterprofile,
                "gameownerships_by_completion_status_list": gameownerships_by_completion_status_list,
                "completion_status_update_form": CompletionStatusUpdateForm
            }
        )

class AddGamesView(LoginRequiredMixin, ListView):
    template_name = 'profiles/add_games.html'
    context_object_name = 'add_game_forms'

    def get_queryset(self):
        unaffiliated_games = self.request.user.gamebeaterprofile.get_unaffiliated_games()
        ownership_list = []
        for game in unaffiliated_games:
            ownership = GameOwnershipForm(
                {"game": game, "owner": self.request.user.gamebeaterprofile}
            )
            ownership.fields['platform'].queryset = ownership.data['game'].platforms
            ownership_list.append(ownership)
        return tuple(ownership_list)

class PreventGetMixin():
    """
    This mixin allows views to always refuse get requests. This is useful
    when a view should only process a POST and not display a form.
    """
    def get(self, request, *args, **kwargs):
        raise Http404

class GameOwnershipCreationView(LoginRequiredMixin, PreventGetMixin, CreateView):
    model = GameOwnership
    form_class = GameOwnershipForm

    success_url = reverse_lazy("profiles:add_games")

class GameOwnershipUpdateView(LoginRequiredMixin, UpdateView):
    model = GameOwnership
    form_class = GameOwnershipUpdateForm
    context_object_name = 'ownership_object'
    template_name = 'profiles/gameownership_update.html'

    success_url = reverse_lazy("profiles:dashboard")

    def get(self, request, *args, **kwargs):
        context_object = self.get_object()
        update_form = GameOwnershipUpdateForm(instance=context_object)
        update_form.fields['platform'].queryset = context_object.game.platforms
        return render(
            request,
            'profiles/gameownership_update.html',
            {
                "update_form": update_form,
                self.context_object_name: context_object
            }
        )

class GameOwnershipDeletionView(LoginRequiredMixin, DeleteView):
    model = GameOwnership
    success_url = reverse_lazy('profiles:dashboard')

class GoalDeletionView(LoginRequiredMixin, DeleteView):
    model = Goal
    success_url = reverse_lazy('profiles:dashboard')

class GoalDashboardView(LoginRequiredMixin, UpdateView):
    model = GameOwnership
    form_class = GoalStatusUpdateForm
    goal_creation_form = GoalCreationForm
    context_object_name = 'ownership_object'
    template_name = 'profiles/goal_dashboard.html'

    #success_url = reverse_lazy("profiles:goal_dashboard", args=[self.kwargs.get(self.pk_url_kwarg)])

    def get(self, request, *args, **kwargs):
        profile_pk = request.user.gamebeaterprofile.pk
        gamebeaterprofile = get_object_or_404(GamebeaterProfile, pk=profile_pk)

        # We have to check that the profile exists before you get the object
        # this could be messed up
        # TODO: change routes to work properly with the profile
        context_object = self.get_object()
        goal_form = self.goal_creation_form(
            {"ownership": context_object.pk}
        )
        goals_by_completion_status_list = get_all_objects_by_status(context_object.goal_set, CompletionStatus, context_object.get_goals_by_completion)
        return render(
            request,
            self.template_name,
            {
                "goal_form": self.form_class,
                self.context_object_name: context_object,
                "goals_by_completion_status_list": goals_by_completion_status_list,
                "goal_creation_form": goal_form
            }
        )

class CompletionStatusUpdateView(LoginRequiredMixin, PreventGetMixin, UpdateView):
    model = GameOwnership
    form_class = CompletionStatusUpdateForm

    success_url = reverse_lazy("profiles:dashboard")

class GoalCompletionStatusUpdateView(LoginRequiredMixin, PreventGetMixin, UpdateView):
    model = Goal
    form_class = GoalCompletionStatusUpdateForm

    success_url = reverse_lazy("profiles:dashboard")

def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)

        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            gamebeater_profile = GamebeaterProfile(user=user)
            gamebeater_profile.save()

            registered = True

        else:
            print user_form.errors
    else:
        user_form = UserForm()

    return render(
        request,
        'profiles/register.html',
        {'user_form': user_form, 'registered': registered}
    )

class CreateGoalView(LoginRequiredMixin, CreateView):
    model = GameOwnership
    form_class = GoalCreationForm

    success_url = reverse_lazy("profiles:dashboard")