resource "aws_route53_record" "domain" {
  name    = "${aws_api_gateway_domain_name.dogs.domain_name}"
  type    = "A"
  zone_id = "${var.zone_id}"

  alias {
    evaluate_target_health = true
    name                   = "${aws_api_gateway_domain_name.dogs.cloudfront_domain_name}"
    zone_id                = "${aws_api_gateway_domain_name.dogs.cloudfront_zone_id}"
  }
}