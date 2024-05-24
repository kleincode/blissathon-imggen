curl -X POST \
    -H "Authorization: Bearer $(gcloud auth print-access-token)" \
    -H "Content-Type: application/json; charset=utf-8" \
    -d @request.json \
    "https://us-central1-aiplatform.googleapis.com/v1/projects/bliss-hack24ber-6526/locations/us-central1/publishers/google/models/imagegeneration:predict" > response.json