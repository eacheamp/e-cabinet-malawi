from django import forms


from .models import Motion

class MotionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MotionForm, self).__init__(*args, **kwargs)
        self.fields['summary'].disabled = True

    class Meta:
        model = Motion
        fields = ('title', 'ministry', 'pdf')
        widgets = {
            'id': forms.HiddenInput(),
            'summary': forms.HiddenInput(),
            'cabinet_vote': forms.HiddenInput(),
            'chair_vote': forms.HiddenInput(),
            'Votes_Favor': forms.HiddenInput(),
            'Votes_Against': forms.HiddenInput(),
            'Votes_Nodesc': forms.HiddenInput(),
            'final_vote': forms.HiddenInput(),
            }






