import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import numpy as np
import requests
from io import BytesIO
import csv
import json
from collections import defaultdict

store = defaultdict(int)

bootstrap = """<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.0/css/bootstrap.min.css">
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.0/js/bootstrap.min.js"></script>
"""

image_template = """
<div class="well text-center">
    <div class="row">
        <div class="col-md-4">
            <img style="width:500px" src="{}">
        </div>
        <div class="col-md-4">
            <img style="width:500px" src="{}">
        </div>
    </div>
</div>
"""

title_template = """
<h4>{}<mark>{}</mark></h4> 
"""

line_template = """
<p>{}</p>
"""

box_template = """
<h4><mark>[detection: box {}]</mark></h4> 
"""

intent_questions = {
    "mp1_feel": "How might MP1 feel after seeing this edit?",
    "mp2_feel": "How might MP2 feel after seeing this edit?",
    # "mp3_purpose": "What does Editor think about MP3?",
    "mp3_feel": "How might MP2 feel after seeing this edit?",
    "intent": "Why did Editor create this edit?",
    "implications": "What are the possible implications of this edit?"
    # "mp3_reaction": "How might MP3 feel after seeing this edit?"
}

org_templates = ['This edit could potentially be used to ', 'Editor created this edit to ', 'Editor created this edit to', 'MP1 would', 'MP2 would', 'MP3 would']

running_website = "" + bootstrap

input_files = ['batch.csv']# ['Batch_3908447_batch_results.csv', 'Batch_3904853_batch_results.csv', 'Batch_3906965_batch_results.csv', 'Batch_3908920_batch_results.csv', 'Batch_3907743_batch_results.csv']
writefile_name = 'batch-review-2-16.html'

for input_file in input_files:
    with open(input_file) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for idx, row in enumerate(csv_reader):
            image_o = row['Input.image_o']
            image_boxes = row['Input.image_b']
            # uncomment to generate
            running_website += "<b> assignment: XXXXXXXXXXXXXXX" + row["AssignmentId"][-8:] + "</b> \n"
            running_website += image_template.format(image_o, image_boxes)
            # running_website += image_template.format(image_o, 'https://jeffda.com/research/part3b/{}.png'.format(idx))
            for item in intent_questions:
                title = item
                current_paragraph = ""
                for idx in ['0', '1', '2']:
                    response = 'Answer.' + title + '_' + idx
                    response = row[response]
                    if response is not '{}' and len(response) > 0 and response not in org_templates:
                        current_paragraph += line_template.format(response)
                if current_paragraph != "":
                    box_label = ""
                    if "_feel" in title:
                        mp_what = title[2]
                        box_num = row["Answer.mp" + mp_what + "_box"]
                        box_label = box_template.format(box_num)
                    running_website += title_template.format(intent_questions[title], '[dim: ' + title.replace("feel", "effects") + ']') + box_label + current_paragraph
            pos_neg_tf = row["Answer.pos_neg_tf"]
            running_website += title_template.format("poor portrayal? ", pos_neg_tf)

output_file = open(writefile_name, 'w')
output_file.write(running_website)