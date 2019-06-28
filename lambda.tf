module "python_lambda_archive" {
    source      = "rojopolis/lambda-python-archive/aws"
    src_dir     = "${path.module}/src"
    output_path = "${path.module}/lambda.zip"
}

resource "aws_iam_role" "iam_for_lambda" {
  name = "iam_for_lambda"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": [
          "apigateway.amazonaws.com",
          "lambda.amazonaws.com"
        ]
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}
data "aws_iam_policy_document" "lamdagw" {
  statement {
    effect = "Allow"

    actions = [
       "logs:CreateLogStream",
       "logs:PutLogEvents"
    ]

    resources = [
      "arn:aws:logs:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:*"
    ]
  }
}

resource "aws_iam_policy" "policy" {
  name        = "lambda_allow_logging"
  description = "A Policy to allow lambda to log"
  policy = "${data.aws_iam_policy_document.lamdagw.json}"
}
resource "aws_iam_role_policy_attachment" "test-attach" {
  role       = "${aws_iam_role.iam_for_lambda.name}"
  policy_arn = "${aws_iam_policy.policy.arn}"
}