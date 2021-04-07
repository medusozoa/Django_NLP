from django.shortcuts import render
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
from allennlp.predictors.predictor import Predictor
import allennlp_models.rc

predictor = Predictor.from_path(
    "https://storage.googleapis.com/allennlp-public-models/bidaf-elmo.2021-02-11.tar.gz")


class NewTextForm(forms.Form):
    text = forms.CharField(label=False, widget=forms.Textarea)


class NewQuestionFrom(forms.Form):
    question = forms.CharField(label="Question")


myquestion = ""
mytext = ""



# Create your views here.
def index(request):
    if "Text" not in request.session:
        request.session["Text"] = ""

    if "QuestionSession" not in request.session:
        request.session["QuestionSession"] = ""

    if "AnswerSession" not in request.session:
        request.session["AnswerSession"] = ""

    return render(request, "QandA/index.html", {
        "Text": request.session["Text"],
        "QuestionSession": request.session["QuestionSession"],
        "AnswerSession": request.session["AnswerSession"]
    })


def addText(request):
    if request.method == "POST":
        form = NewTextForm(request.POST)

        if form.is_valid():
            text = form.cleaned_data["text"]
            request.session["Text"] = text
            global mytext
            mytext = text
            return HttpResponseRedirect(reverse("QandA:index"))

        else:
            return render(request, "QandA/addText.html", {
                "form": form
            })

    return render(request, "QandA/addText.html", {
        "form": NewTextForm()
    })


def addQuestion(request):
    if request.method == "POST":
        form = NewQuestionFrom(request.POST)

        if form.is_valid():
            question = form.cleaned_data["question"]
            request.session["QuestionSession"] = question
            global myquestion
            myquestion = question
            request.session["AnswerSession"] = answer()
            return HttpResponseRedirect(reverse("QandA:index"))

        else:
            return render(request, "QandA/addQuestion.html", {
                "form": form
            })

    return render(request, "QandA/addQuestion.html", {
        "form": NewQuestionFrom()
    })


def answer():
    d = predictor.predict(
        passage=mytext,
        question=myquestion
    )
    res = d['best_span_str']

    return res


def changer1(item):
    return item + "changer"
