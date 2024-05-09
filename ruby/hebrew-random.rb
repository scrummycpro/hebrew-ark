require 'uri'
require 'net/http'
require 'json'

def fetch_random_text
  url = URI("https://www.sefaria.org/api/texts/random-by-topic")

  http = Net::HTTP.new(url.host, url.port)
  http.use_ssl = true

  request = Net::HTTP::Get.new(url)
  request["accept"] = 'application/json'

  response = http.request(request)
  puts "Raw Response Body: #{response.body}" # Debugging output
  JSON.parse(response.body)
end

def fetch_text_content(url)
  if url.start_with?('http')
    uri = URI(url)

    http = Net::HTTP.new(uri.host, uri.port)
    http.use_ssl = true

    request = Net::HTTP::Get.new(uri)
    request["accept"] = 'application/json'

    response = http.request(request)
    JSON.parse(response.body)
  else
    raise "Invalid URL: #{url}"
  end
end

def display_result(result)
  if result.key?('url')
    begin
      text_content = fetch_text_content(result['url'])
      puts "\e[34mTitle:\e[0m #{text_content['title']}"
      puts "\e[32mText:\e[0m #{text_content['he']}"
    rescue StandardError => e
      puts "\e[31mAn error occurred: #{e.message}\e[0m"
    end
  else
    puts "\e[31mError: Could not fetch data from the API.\e[0m"
  end
end

def main
  begin
    result = fetch_random_text
    display_result(result)
  rescue StandardError => e
    puts "\e[31mAn error occurred: #{e.message}\e[0m"
  end
end

main
