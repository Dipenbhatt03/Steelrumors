import json
from django.utils.timezone import now
from django.http import HttpResponse
from django.db.models import  Count
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.core.urlresolvers import reverse_lazy
from django.core.urlresolvers import reverse
from django.views.generic import  ListView
from django.views.generic import DetailView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.views.generic.edit import CreateView
from django.views.generic.edit import FormView
from django.contrib.auth import  get_user_model
from models import  Link,UserProfile,Vote
from forms import UserProfileForm
from forms import LinkCreateForm
from forms import VoteForm



class LinkListView(ListView):
    model = Link
    template_name = "link_list.html"
    paginate_by = 5
    queryset = Link.with_votes.all()
    #def get_queryset(self):
     #   return super(LinkListView,self).get_queryset().annotate(votes=Count('vote')).order_by('-votes')
    def get_context_data(self, **kwargs):
        context=super(LinkListView,self).get_context_data(**kwargs)
        if self.request.user.is_authenticated():
            voted=Vote.objects.filter(voter=self.request.user)
            links_in_page=[]
            for link in context["object_list"]:
                links_in_page.append(link.id)
            voted=voted.filter(link_id__in=links_in_page)
            voted=voted.values_list('link_id',flat=True)
            context["voted"]=voted
        return context

class LinkCreateView(CreateView):
    model = Link
    form_class = LinkCreateForm
    template_name = 'link_form.html'
    def form_valid(self, form):
        form.instance.submitter=self.request.user
        form.instance.rank_scores=0
        return super(LinkCreateView,self).form_valid(form)


class LinkDetailView(DetailView):
    model = Link
    template_name = 'link_detail.html'

class LinkUpdateView(UpdateView):
    model = Link
    form_class = LinkCreateForm
    template_name = 'link_form.html'

class LinkDeleteView(DeleteView):
    model = Link
    template_name = 'link_confirm_delete.html'
    success_url = reverse_lazy("home")


class UserProfileDetailView(DetailView):
    model = get_user_model()
    template_name = 'user_detail.html'
    slug_field = 'username'
    def get_object(self, queryset=None):
        user=super(UserProfileDetailView,self).get_object(queryset)
        UserProfile.objects.get_or_create(user=user)
        return  user

class UserProfileEditView(UpdateView):
    model = UserProfile
    template_name = "edit_profile.html"
    form_class = UserProfileForm
    def get_object(self, queryset=None):
        return UserProfile.objects.get_or_create(user=self.request.user)[0] #[0] because this function returns 2 values and we need the first
    def get_success_url(self):
        return reverse("profile",kwargs={"slug":self.request.user})

class JSONFormMixin(object):
    def create_response(self,vdict=dict(),valid_form=True):
        response=HttpResponse(json.dumps(vdict),content_type="application/json")
        response.status_code=200 if valid_form else 500
        return response


class VoteFormView(FormView):
    form_class = VoteForm
    template_name = 'link_list.html'
    def form_valid(self, form):
        user=self.request.user
        link=get_object_or_404(Link,pk=form.data["link"])
        num_votes=Vote.objects.filter(voter=user,link=link)
        val = self.request.POST.get('bt1')
        if val=="downvote":
            num_votes[0].delete()
        elif val=="upvote":
            Vote.objects.create(voter=user,link=link)
        return redirect("home")
'''

    def create_response(self,vdict=dict(),valid_form=True):
        response=HttpResponse(json.dump(vdict))
        response.status_code = 200 if valid_form else 500
        return response

    def form_valid(self, form):
        user=self.request.user
        link=get_object_or_404(Link,pk=form.data["link"])
        prev_votes=Vote.objects.filter(voter=user,link=link)
        has_voted=(prev_votes.count()>0)
        ret={'success':1}

        if not has_voted:
            v=Vote.objects.create(voter=user,link=link)
            ret['voteobj']=v.id
        else:
            prev_votes[0].delete()
            ret['unvoted']=1
        return self.create_response(ret,True)
    def form_invalid(self, form):
        ret={"success":0,"form_errors":form.errors}
        return self.create_response(ret,False)
'''

#class VoteFormView(JSONFormMixin,VoteFormBaseView):
 #   pass


