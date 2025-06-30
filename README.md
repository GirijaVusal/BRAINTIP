# Access the API

### For tool calling:
http://0.0.0.0:8080/api/chat/tool

Auth: Bearer d6ca11a82f5c0c0d65c33f1c32fd96dea7ceb3b91be8b2a488da75f7be0ecbd3

Payload: {
  "user_query": "temperature of kathmandu"
}

Payload: {
  "user_query": "what is 2*8-2"
}

### For Riddle: 

    Prompt: 

    Your task is to reverse this process: given a reversed, fused animal word, determine the two original animals whose name beginnings were fused together.

    Process:
      1. Reverse the input string.
      2. Try to split the reversed string into two valid animal name beginnings.
      3. Guess the most likely full animal names based on common animals.

    For example:
      If the input word is ['barlow'] 
      Its expected output is = wolf + rabbit
      Strictly follow the format for your final output.
    

    ## Output format:
    The output should be concise, in parsable JSON format.
    Always give final output in json only no explanation needed:
    "barlow":["wolf","rabbit"]

    ## Riddle To solve:
       {}

    Final output: 

Endpoint: http://0.0.0.0:8080/api/chat/riddle

Auth: Bearer d6ca11a82f5c0c0d65c33f1c32fd96dea7ceb3b91be8b2a488da75f7be0ecbd3

Payload:{
  "user_query": "solve this riddle: Aebrib"
}

