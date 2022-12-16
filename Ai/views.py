from django.shortcuts import render, HttpResponse
from django.conf import settings
from django.core.mail import send_mail

from .forms import MyfileUploadForm
from .models import file_upload
import pandas as pd
import openai
import numpy as np
# import matplotlib.pyplot as plt
from openai.embeddings_utils import cosine_similarity
import json
from sklearn.decomposition import PCA

# from scipy import spatial

import plotly.express as px


def index(request):
    if request.method == 'POST':
        form = MyfileUploadForm(request.POST, request.FILES)



        if form.is_valid():
            name = form.cleaned_data['file_name']
            the_files = form.cleaned_data['files_data']

            df = pd.read_csv(the_files)

            df = df[['salary', 'position', 'experience', 'formOfCooperation', 'technologies', 'databases', 'changeIf']]
            df = df.dropna()



            df['combined'] = "Title: " + df.position.str.strip() + "; Experience: " + df.experience.str.strip() + "; technologies :" + df.technologies.str.strip()
            openai.api_key = "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"
            #
            def get_embedding(text, model="text-similarity-davinci-001"):
                text = text.replace("\n", " ")
                return openai.Embedding.create(input=[text], model=model)['data'][0]['embedding']
            #
            # # df.head(10)
            df['babbage_similarity'] = df.combined.apply(
                lambda x: get_embedding(x, model='text-similarity-babbage-001'))

            df['babbage_search'] = df.combined.apply(lambda x: get_embedding(x, model='text-search-babbage-doc-001'))

            position = request.POST.get('title')

            experience = request.POST.get('experience')
            technologies = request.POST.get('technology')
            final = position+ ' ' + experience +' '+ technologies

            print(final)

            def search_reviews(df, product_description, n=3, pprint=True):

                embedding = get_embedding(
                    product_description,
                    model="text-search-babbage-query-001"
                )

                df["similarities"] = df.babbage_search.apply(lambda x: cosine_similarity(x, embedding))

                res = (
                    df.sort_values("similarities", ascending=False)
                        .head(n)

                )

                return res

            res = search_reviews(df, final, n=3)
            print(res)
            json_records = res.reset_index().to_json(orient='records')

            data = json.loads(json_records)
            context = {'d': data}


            file_upload(file_name=name, my_file=the_files).save()

            return render(request,'results.html',context)
        else:
            return HttpResponse('error')

    else:

        context = {
            'form': MyfileUploadForm()
        }

        return render(request, 'index.html', context)


def show_file(request):

    all_data = file_upload.objects.all()

    context = {
        'data': all_data
    }

    return render(request, 'view.html', context)
def result(request):
    return render(request, 'results.html')
def s_email(request):
    if 'back' in request.POST:
        return render(request,'index.html')

    subject = 'JOB ALERT'

    message = "Software Company\n123 Main Street\nSan Francisco, CA 94102\nDate: January 1, 2021\n\nDear [Candidate],\n\n We are pleased to offer you the position of [Position] at Software Company. We were impressed by your skills , experience and believe you would be a valuable addition to our team\n\n We hope you will accept this offer and join our team. Please let us know if you have any questions or need any additional information.\n\nSincerely,\nVulcaints"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['wasifsaeed970@gmail.com','maksym.wolff@newnative.ai','qasimvirk90@gmail.com']
    send_mail(subject, message, email_from, recipient_list)
    return render(request,'contact.html')
