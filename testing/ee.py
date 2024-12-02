from rapidfuzz import fuzz

words = ['start', 'date', 'dc', 'id', 'distribution', 'center', 'conroe', 'city', 'category', 'sunglasses']
aa = {
  "entities": [
    {
      "entity": "amount qty",
      "column name": "aa_qty",
      "column datatype": "number",
      "column description": "This column represents the amount quantity",
    },
    {
      "entity": "typecode",
      "column name": "MSD_TYPE_CD",
      "column datatype": "number",
      "column description": "This column represents the type code",
    },
    {
      "entity": "distribution center id",
      "column name": "dc_id",
      "column datatype": "number",
      "column description": "This column represents the distribution center id",
    },
    {
      "entity": "sales end date",
      "column name": "SALES_END_DT",
      "column datatype": "Date",
      "column description": "This column represents the sales end billing date",
    },
    {
      "entity": "sales start date",
      "column name": "SALES_START_DT",
      "column datatype": "Date",
      "column description": "This column represents the sales start billing date",
    },
  ]
}

def calculate_fuzz_scores(word, metadata):
    scores = {}
    for key, value in metadata.items():
        if isinstance(value, str):
            score = fuzz.token_set_ratio(word, value)
            scores[key] = score
    return scores

for word in words:
    print(f"Scores for word '{word}':")
    for entity in aa["entities"]:
        entity_scores = calculate_fuzz_scores(word, entity)
        print(entity_scores)
    print()





scores

Scores for word 'start':
{'entity': 26.66666666666667, 'column name': 36.36363636363637, 'column datatype': 18.181818181818187, 'column description': 21.276595744680847}
{'entity': 15.384615384615387, 'column name': 0.0, 'column datatype': 18.181818181818187, 'column description': 14.63414634146342}
{'entity': 29.629629629629633, 'column name': 0.0, 'column datatype': 18.181818181818187, 'column description': 14.81481481481481}
{'entity': 21.05263157894737, 'column name': 0.0, 'column datatype': 44.44444444444444, 'column description': 14.81481481481481}
{'entity': 100.0, 'column name': 0.0, 'column datatype': 44.44444444444444, 'column description': 100.0}

Scores for word 'date':
{'entity': 28.57142857142857, 'column name': 40.0, 'column datatype': 20.0, 'column description': 13.043478260869563}
{'entity': 33.33333333333333, 'column name': 0.0, 'column datatype': 20.0, 'column description': 15.0}
{'entity': 15.384615384615387, 'column name': 22.22222222222223, 'column datatype': 20.0, 'column description': 11.320754716981128}
{'entity': 100.0, 'column name': 0.0, 'column datatype': 75.0, 'column description': 100.0}
{'entity': 100.0, 'column name': 0.0, 'column datatype': 75.0, 'column description': 100.0}

Scores for word 'dc':
{'entity': 0.0, 'column name': 0.0, 'column datatype': 0.0, 'column description': 4.545454545454547}
{'entity': 20.0, 'column name': 0.0, 'column datatype': 0.0, 'column description': 10.526315789473685}
{'entity': 8.333333333333329, 'column name': 57.142857142857146, 'column datatype': 0.0, 'column description': 3.9215686274509807}
{'entity': 12.5, 'column name': 0.0, 'column datatype': 0.0, 'column description': 3.9215686274509807}
{'entity': 11.111111111111114, 'column name': 0.0, 'column datatype': 0.0, 'column description': 3.773584905660371}

Scores for word 'id':
{'entity': 0.0, 'column name': 0.0, 'column datatype': 0.0, 'column description': 4.545454545454547}
{'entity': 20.0, 'column name': 0.0, 'column datatype': 0.0, 'column description': 10.526315789473685}
{'entity': 100.0, 'column name': 57.142857142857146, 'column datatype': 0.0, 'column description': 100.0}
{'entity': 12.5, 'column name': 0.0, 'column datatype': 0.0, 'column description': 7.843137254901961}
{'entity': 11.111111111111114, 'column name': 0.0, 'column datatype': 0.0, 'column description': 7.547169811320757}

Scores for word 'distribution':
{'entity': 18.181818181818187, 'column name': 11.111111111111114, 'column datatype': 11.111111111111114, 'column description': 25.925925925925924}
{'entity': 20.0, 'column name': 0.0, 'column datatype': 11.111111111111114, 'column description': 16.66666666666667}
{'entity': 100.0, 'column name': 23.529411764705884, 'column datatype': 11.111111111111114, 'column description': 100.0}
{'entity': 23.07692307692308, 'column name': 0.0, 'column datatype': 12.5, 'column description': 19.67213114754098}
{'entity': 35.71428571428571, 'column name': 0.0, 'column datatype': 12.5, 'column description': 19.04761904761905}

Scores for word 'center':
{'entity': 25.0, 'column name': 16.66666666666667, 'column datatype': 50.0, 'column description': 20.83333333333333}
{'entity': 28.57142857142857, 'column name': 0.0, 'column datatype': 50.0, 'column description': 23.80952380952381}
{'entity': 100.0, 'column name': 18.181818181818187, 'column datatype': 50.0, 'column description': 100.0}
{'entity': 30.0, 'column name': 0.0, 'column datatype': 40.0, 'column description': 18.181818181818187}
{'entity': 27.272727272727266, 'column name': 0.0, 'column datatype': 40.0, 'column description': 21.05263157894737}

Scores for word 'conroe':
{'entity': 25.0, 'column name': 0.0, 'column datatype': 33.33333333333333, 'column description': 20.83333333333333}
{'entity': 42.857142857142854, 'column name': 0.0, 'column datatype': 33.33333333333333, 'column description': 23.80952380952381}
{'entity': 28.57142857142857, 'column name': 18.181818181818187, 'column datatype': 33.33333333333333, 'column description': 21.818181818181813}
{'entity': 20.0, 'column name': 0.0, 'column datatype': 20.0, 'column description': 18.181818181818187}
{'entity': 9.090909090909093, 'column name': 0.0, 'column datatype': 20.0, 'column description': 17.54385964912281}

Scores for word 'city':
{'entity': 28.57142857142857, 'column name': 40.0, 'column datatype': 0.0, 'column description': 17.391304347826093}
{'entity': 33.33333333333333, 'column name': 0.0, 'column datatype': 0.0, 'column description': 15.0}
{'entity': 23.07692307692308, 'column name': 44.44444444444444, 'column datatype': 0.0, 'column description': 11.320754716981128}
{'entity': 11.111111111111114, 'column name': 0.0, 'column datatype': 25.0, 'column description': 7.547169811320757}
{'entity': 10.0, 'column name': 0.0, 'column datatype': 25.0, 'column description': 7.272727272727266}

Scores for word 'category':
{'entity': 33.33333333333333, 'column name': 42.857142857142854, 'column datatype': 28.57142857142857, 'column description': 20.0}
{'entity': 37.5, 'column name': 0.0, 'column datatype': 28.57142857142857, 'column description': 22.727272727272734}
{'entity': 26.66666666666667, 'column name': 15.384615384615387, 'column datatype': 28.57142857142857, 'column description': 17.54385964912281}
{'entity': 27.272727272727266, 'column name': 0.0, 'column datatype': 50.0, 'column description': 17.54385964912281}
{'entity': 33.33333333333333, 'column name': 0.0, 'column datatype': 50.0, 'column description': 16.949152542372886}

Scores for word 'sunglasses':
{'entity': 20.0, 'column name': 12.5, 'column datatype': 25.0, 'column description': 30.769230769230774}
{'entity': 11.111111111111114, 'column name': 0.0, 'column datatype': 25.0, 'column description': 26.086956521739125}
{'entity': 18.75, 'column name': 0.0, 'column datatype': 25.0, 'column description': 23.728813559322035}
{'entity': 33.33333333333333, 'column name': 0.0, 'column datatype': 28.57142857142857, 'column description': 30.508474576271183}
{'entity': 30.769230769230774, 'column name': 0.0, 'column datatype': 28.57142857142857, 'column description': 29.508196721311478}

````````````````````````

import os
import json
from rapidfuzz import fuzz
from tqdm import tqdm

def process_metadata(datadictionary_path, keywords, threshold=50):
    final_results = []

    # Iterate through all JSON files in the datadictionary folder
    json_files = [f for f in os.listdir(datadictionary_path) if f.endswith('.json')]

    for json_file in tqdm(json_files, desc="Processing JSON files"):
        file_path = os.path.join(datadictionary_path, json_file)

        # Load JSON content
        with open(file_path, 'r') as f:
            metadata = json.load(f)

        table_name = metadata['table_name']
        database_name = metadata['database name']
        schema_name = metadata['schema']
        entities = metadata['entities']

        for keyword in keywords:
            for entity in entities:
                result = {}

                fields_to_compare = {
                    "entity": entity["entity"],
                    "columnname": entity["column name"],
                    "columndatatype": entity["column datatype"],
                    "columndescription": entity["column description"],
                }

                for field, value in fields_to_compare.items():
                    score = fuzz.ratio(keyword.lower(), str(value).lower())
                    rounded_score = round(score, 2)
                    result[field] = [value, rounded_score]

                # If any score exceeds the threshold, add to final results
                if any(score[1] > threshold for score in result.values()):
                    matched_fields = {
                        "keyword": keyword,
                        "table_name": table_name,
                        "database_name": database_name,
                        "schema_name": schema_name,
                        "matches": result,
                    }
                    final_results.append(matched_fields)

    return final_results

# Input details
datadictionary_path = "./datadictionary"  # Update the path to your datadictionary folder
keywords = ['start', 'date', 'dc', 'id', 'distribution', 'center', 'conroe', 'city', 'category', 'sunglasses']
threshold = 50

# Run the function
results = process_metadata(datadictionary_path, keywords, threshold)

# Display final results
print("Matching Metadata Fields:")
for item in results:
    print(json.dumps(item, indent=2))
