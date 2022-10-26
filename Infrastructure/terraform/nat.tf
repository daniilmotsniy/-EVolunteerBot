# resource "aws_eip" "nat" {
#   vpc        = true
#   depends_on = [aws_internet_gateway.internet-gw]
# }

# resource "aws_nat_gateway" "nat-gw" {
#   allocation_id     = aws_eip.nat.id
#   subnet_id         = aws_subnet.public.id
#   depends_on        = [aws_internet_gateway.internet-gw]
#   connectivity_type = "public"
# }

# resource "aws_route_table" "private-rt" {
#   vpc_id = aws_vpc.vpc_main.id
#   route {
#     cidr_block     = "0.0.0.0/0"
#     nat_gateway_id = aws_nat_gateway.nat-gw.id
#   }
# }

# resource "aws_route_table_association" "private-rta" {
#   subnet_id      = aws_subnet.private.id
#   route_table_id = aws_route_table.private-rt.id
# }