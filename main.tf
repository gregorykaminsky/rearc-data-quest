
provider "archive" {}
#data "archive_file" "zip" {
#  type        = "zip"
#  source_file = "rearc_lambda.py"
#  output_path = "rearc_lambda.zip"
#}


data "aws_iam_policy_document" "policy" {
  statement {
    sid    = ""
    effect = "Allow"
    principals {
      identifiers = ["lambda.amazonaws.com"]
      type        = "Service"
    }
    actions = ["sts:AssumeRole"]
  }
}
resource "aws_iam_role" "iam_for_lambda" {
  name               = "iam_for_lambda"
  assume_role_policy = data.aws_iam_policy_document.policy.json
}

resource "aws_lambda_function" "lambda" {
  function_name = "rearc_lambda"
  #filename         = data.archive_file.zip.output_path
  filename = "rearc_lambda.zip"
  #source_code_hash = data.archive_file.zip.output_base64sha256
  role    = aws_iam_role.iam_for_lambda.arn
  handler = "rearc_lambda.lambda_handler"
  runtime = "python3.9"
  timeout = 300

    environment {
    variables = {
        aws_access_key = var.aws_access_key
        aws_secret_key = var.aws_secret_key
    }
    }
}

resource "aws_cloudwatch_event_rule" "once_a_day" {
  name                = "once_a_day"
  description         = "Fires once a day"
  #schedule expression for once a day at 12:00pm UTC
  schedule_expression = "cron(0 12 * * ? *)"
}

resource "aws_cloudwatch_event_target" "check_foo_once_a_day" {
  rule      = "${aws_cloudwatch_event_rule.once_a_day.name}"
  target_id = "lambda"
  arn       = "${aws_lambda_function.lambda.arn}"
}

resource "aws_lambda_permission" "allow_cloudwatch_to_call_check_foo" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = "${aws_lambda_function.lambda.function_name}"
  principal     = "events.amazonaws.com"
  source_arn    = "${aws_cloudwatch_event_rule.once_a_day.arn}"
}