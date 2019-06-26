resource "aws_lambda_function" "breeds_list_lambda" {
  filename         = "${module.python_lambda_archive.archive_path}"
  function_name    = "dog-api-breedlist"
  role             = "${aws_iam_role.iam_for_lambda.arn}"
  handler          = "handler.breeds"
  source_code_hash = "${module.python_lambda_archive.source_code_hash}"
  runtime          = "python3.6"
  environment {
    variables = {
      use_reddit          = "${var.use_reddit}"
      access_token_secret = "${var.access_token_secret}"
      reddit_clientID     = "${var.reddit_clientID}"
      reddit_clientsec    = "${var.reddit_clientsec}"
      reddit_pass         = "${var.reddit_pass}"
      reddit_user         = "${var.reddit_user}"
    }
  }
}
resource "aws_api_gateway_resource" "breed_list_resource" {
  path_part   = "breed"
  parent_id   = "${aws_api_gateway_rest_api.api.root_resource_id}"
  rest_api_id = "${aws_api_gateway_rest_api.api.id}"
}

resource "aws_api_gateway_method" "breed_list_method" {
  rest_api_id   = "${aws_api_gateway_rest_api.api.id}"
  resource_id   = "${aws_api_gateway_resource.breed_list_resource.id}"
  http_method   = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "breed_list_integration" {
  rest_api_id             = "${aws_api_gateway_rest_api.api.id}"
  resource_id             = "${aws_api_gateway_resource.breed_list_resource.id}"
  http_method             = "${aws_api_gateway_method.breed_list_method.http_method}"
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = "arn:aws:apigateway:${data.aws_region.current.name}:lambda:path/2015-03-31/functions/${aws_lambda_function.breeds_list_lambda.arn}/invocations"
}

# Lambda
resource "aws_lambda_permission" "apigw_lambda_breed_list" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = "${aws_lambda_function.breeds_list_lambda.function_name}"
  principal     = "apigateway.amazonaws.com"
  source_arn = "arn:aws:execute-api:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:*"
}