output "api_url" {
  description = "Base URL of the HTTP API"
  value       = aws_apigatewayv2_api.http.api_endpoint
}

output "table_name" {
  description = "DynamoDB table name"
  value       = aws_dynamodb_table.items.name
}

output "function_name" {
  description = "Lambda function name"
  value       = aws_lambda_function.api.function_name
}
