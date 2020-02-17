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
    "intent": "Why did Editor create this edit?",
    "implications": "What are the possible implications of this edit?"
    # "mp3_reaction": "How might MP3 feel after seeing this edit?"
}

org_templates = ['This edit could potentially be used to ', 'Editor created this edit to ', 'Editor created this edit to', 'MP1 would', 'MP2 would', 'MP3 would']

running_website = "" + bootstrap

input_files = ['output.csv'] # ['Batch_3908447_batch_results.csv', 'Batch_3904853_batch_results.csv', 'Batch_3906965_batch_results.csv', 'Batch_3908920_batch_results.csv', 'Batch_3907743_batch_results.csv']

store = {}

for input_file in ['dev_set.csv']:
    with open(input_file) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for idx, row in enumerate(csv_reader):
            idx = int(row["image_b"].split("_")[0].split('/')[-1])
            store[idx] = row["image_o"]

for input_file in input_files:
    with open(input_file) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for idx, row in enumerate(csv_reader):
            image_o = store[int(row['image_index'])]
            image_boxes = 'https://jeffda.com/research/part4/' + row['image_index'] + '_boxes.jpg'
            # uncomment to generate
            running_website += image_template.format(image_o, image_boxes)
            # running_website += image_template.format(image_o, 'https://jeffda.com/research/part3b/{}.png'.format(idx))
            for item in intent_questions:
                title = item
                current_paragraph = ""
                for idx in ['0', '1', '2']:
                    response = title + '_' + idx
                    response = row[response].replace("!", "").replace("MP1 would ", "MP would ")
                    if response is not '{}' and len(response) > 0 and response not in org_templates:
                        current_paragraph += line_template.format(response)
                running_website += current_paragraph

output_file = open('index.html', 'w')
output_file.write(running_website)