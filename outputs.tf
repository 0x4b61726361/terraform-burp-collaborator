output "private_ip" {
  description = "The private IP address of the collaborator server."
  value = "${aws_instance.collaborator.private_ip}"
}

output "public_ip" {
  description = "The public IP address of the collaborator server."
  value = "${aws_instance.collaborator.public_ip}"
}

output "public_dns" {
  description = "The AWS domain name entry of the collaborator server."
  value = "${aws_instance.collaborator.public_dns}"
}
