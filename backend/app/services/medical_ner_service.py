from transformers import AutoTokenizer, AutoModelForTokenClassification
import torch

tokenizer = AutoTokenizer.from_pretrained("samrawal/bert-base-uncased_clinical-ner")
model = AutoModelForTokenClassification.from_pretrained("samrawal/bert-base-uncased_clinical-ner")

def recognize_medical_entities(text: str):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    outputs = model(**inputs)
    predictions = torch.argmax(outputs.logits, dim=2)
    
    entities = []
    for i, prediction in enumerate(predictions[0]):
        if prediction != 0:  # 0 is the label for 'O' (Outside)
            entity = tokenizer.convert_ids_to_tokens(inputs['input_ids'][0][i])
            label = model.config.id2label[prediction.item()]
            entities.append((entity, label))
    
    return entities