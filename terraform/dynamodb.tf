resource "aws_dynamodb_table" "items" {
  name         = "${var.name}-items"
  billing_mode = "PAY_PER_REQUEST" # on-demand: nothing to provision
  hash_key     = "id"

  attribute {
    name = "id"
    type = "S"
  }

  point_in_time_recovery {
    enabled = true
  }
}
