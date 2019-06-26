variable "domain_name" {}
variable "zone_id" {}

variable "certificate_id" {}

variable "use_reddit" {
  default = false
}
variable "access_token_secret" {
    default = ""
}
variable "reddit_clientID" {
    default = ""
}
variable "reddit_clientsec" {
    default = ""
}
variable "reddit_pass" {
    default = ""
}
variable "reddit_user" {
    default = ""
}
