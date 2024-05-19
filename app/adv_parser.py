import subprocess

token = "{{pat_9PT8qizvohOPkLWYsxkFEzwJxuNQLHuw1RMEEem7P3zLVljQP95t5GHJOpmEnQmo}}"
Bot_Id = 7353668947788611589
Bot_Id = "{{" + str(Bot_Id) + "}}"
query = input()
query = "{{" + query + "}}"
data = {
    "conversation_id": "123",
    "bot_id": f"{Bot_Id}",
    "user": "123333333",
    "query": f"{query}",
    "stream": "false"
}



a = subprocess.Popen("""curl --location --request POST 'https://api.coze.com/open_api/v2/chat' \
--header 'Authorization: Bearer pat_9PT8qizvohOPkLWYsxkFEzwJxuNQLHuw1RMEEem7P3zLVljQP95t5GHJOpmEnQmo' \
--header 'Content-Type: application/json' \
--header 'Accept: */*' \
--header 'Host: api.coze.com' \
--header 'Connection: keep-alive' \
--data-raw '{
    "conversation_id": "123",
    "bot_id": "7353668947788611589",
    "user": "123333333",
    "query": "hello",
    "stream":false
}'""", stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

print(a)
