resource "aws_instance" "api" {
  ami           = var.server_ami
  instance_type = var.api_instance_type
  key_name      = var.key_name
  subnet_id     = aws_subnet.public.id

  user_data = <<EOF
#!/bin/bash -x
apt-get update
apt install -y apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu `lsb_release -cs` test"
sudo apt update
apt install -y docker-ce docker-compose
useradd -m HelpService
cd /home/HelpService/
git clone https://${var.token}@github.com/daniilmotsniy/HelpServiceBE.git
git clone https://${var.token}@github.com/daniilmotsniy/HelpService.git 
git clone https://${var.token}@github.com/daniilmotsniy/HelpServiceFE.git
chown -R HelpService:HelpService HelpService*/
cd HelpServiceBE/
echo -e "MONGODB_URL=mongodb+srv://bayraktar_kharkiv:mMjeONraiEnegzzf@cluster0.hpec3.mongodb.net/myFirstDatabase?retryWrites=true&w=majority" >> .env
echo -e "AWS_ACCESS_KEY_ID=<env>" >> .env
echo -e "AWS_SECRET_ACCESS_KEY=<env>" >> .env
echo -e "BUCKET=pdfkeeper" >> .env
echo -e "AUTH_JWT_ALGORITHM=HS384" >> .env
echo -e "AUTH_JWT_PRIVATE_KEY=XVDYtseRI3FWDxSGYl8qoVbHdL37zyjr" >> .env
echo -e "AUTH_JWT_EXPIRATION_SECONDS=604800" >> .env
echo -e "AUTH_PASSWORD_HASH_SALT=XVDYtseRI3FWDxSGYl8qoVbHdL37zyjr" >> .env
echo -e "AUTH_PASSWORD_HASH_CYCLES=61" >> .env
docker-compose up -d 
cd ../HelpService/
echo -e "MONGODB_URL=<env>" >> .env
echo -e "CITIES=Харків" >> .env
echo -e "BOT_TOKEN=<env>" >> .env
docker-compose up -d
cd ../HelpServiceFE/
docker build -t ui .
docker run -p 3000:3000 --init ui 
EOF

  vpc_security_group_ids = [aws_security_group.api_sec_gr.id]
  tags = {
    "Name"        = "api"
    "Avalability" = "Public"
  }
}
