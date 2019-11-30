data "aws_region" "current" {}
data "aws_caller_identity" "current" {}

resource "aws_api_gateway_rest_api" "api" {
  name = "dog-api"
}

resource "aws_api_gateway_deployment" "main" {
  depends_on = [
      aws_api_gateway_integration.random_integration,
      aws_api_gateway_integration.breed_list_integration,
      aws_api_gateway_integration.breed_integration,
      aws_api_gateway_integration.index_integration
  ]
  rest_api_id = aws_api_gateway_rest_api.api.id
  stage_name  = "prod"
}

resource "aws_api_gateway_client_certificate" "dogs" {
  description = "My client certificate"
}

resource "aws_api_gateway_domain_name" "dogs" {
  domain_name     = "dogs.${var.domain_name}"
  certificate_arn = "arn:aws:acm:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:certificate/${var.certificate_id}"
}
resource "aws_api_gateway_base_path_mapping" "test" {
  api_id      = aws_api_gateway_rest_api.api.id
  stage_name  = aws_api_gateway_deployment.main.stage_name
  domain_name = aws_api_gateway_domain_name.dogs.domain_name
}
