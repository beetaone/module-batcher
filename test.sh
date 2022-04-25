#! /bin/bash

generate_post_data()
{
  cat <<EOF
{
  "temperature":"$((1 + $RANDOM/100))"
}
EOF
}


for ((i=1;i<=500;i++)); do curl --header "Content-Type: application/json" \
  --request POST \
  --data "$(generate_post_data)" \
  http://localhost:5000;

  echo \ -
  done

