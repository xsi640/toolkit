# 认证

# curl -H "Content-Type: application/json" \
#         -d '{"grant_type":"refresh_token", "refresh_token":"'$refresh_token'"}' \
#         https://api.aliyundrive.com/v2/account/token
# 拿到 access_token
#
# 获取 drive_id
# HEADER="Authorization: Bearer $access_token"
# curl -H "$HEADER" -H "Content-Type: application/json" -X POST -d '{}' "https://user.aliyundrive.com/v2/user/get"
#
# 获取文件列表
# curl -H "$HEADER" -H "Content-Type: application/json" -X POST -d '{"drive_id": "'$drive_id'","parent_file_id": "'$file_id'"}' "https://api.aliyundrive.com/adrive/v2/file/list"
# file_id
#
# 获取文件路径
# curl -H "$HEADER" -H "Content-Type: application/json" -X POST -d "{\"drive_id\": \"$drive_id\", \"file_id\": \"$file_id\"}" "https://api.aliyundrive.com/adrive/v1/file/get_path"
#
# 删除文件
# curl --connect-timeout 5 -m 5 -s -H "$HEADER" -H "Content-Type: application/json" -X POST -d '{
#   "requests": [
#     {
#       "body": {
#         "drive_id": "'$drive_id'",
#         "file_id": "'$_file_id'"
#       },
#       "headers": {
#         "Content-Type": "application/json"
#       },
#       "id": "'$_file_id'",
#       "method": "POST",
#       "url": "/file/delete"
#     }
#   ],
#   "resource": "file"
# }' "https://api.aliyundrive.com/v3/batch"