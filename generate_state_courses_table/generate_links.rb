require 'csv'
require 'uri'
require 'net/http'
require "http"
require "rest-client"

def make_request(url)
  result = { url: url }
  response = RestClient::Request.execute(
    method: :get,
    url: url,
    user: AppSetting.setting_value(:ethosce_ws_username),
    password: AppSetting.setting_value(:ethosce_ws_password),
    headers: { 'content-type' => 'application/json', 'accept' => 'application/json' }
  )
  json_response = JSON.parse(response.body)
  if json_response['list'].present?
    result.merge!({
                    status: :success,
                    success: 'Node exists.',
                    response: json_response
                  })
  else
    result.merge!({
                    status: :failure,
                    message: 'Node does not exists.'
                  })
  end
  result
end

puts "Parsing #{ARGV.first}"
data = CSV.read(ARGV.first, headers:true)

username = ""
password = ""

output_filename = '_generated_links.csv'
url_base = "https://education.mocingbird.com"
url_template = "{{domainURL}}"
sso_string = "/user/login?destination="

CSV.open(output_filename, "w") do |csv|
  csv << ["sku", "link", "template_link"]
  data.each do |row|
    if row[5] != nil
	  node_id = row[6]
      node_id.slice! "course_"
      url = "#{url_base}/node.json?nid=" + node_id
      result = { url: url }
      response = RestClient::Request.execute(
        method: :get,
        url: url,
        user: 'restws_production_1',
        password: 'MOC1234',
        headers: { 'content-type' => 'application/json', 'accept' => 'application/json' }
      )
      json_response = JSON.parse(response.body)

      course_link_suffix = json_response['list']&.first&.dig("url")
      course_link_suffix.slice! url_base

      link = "#{url_base}#{sso_string}#{course_link_suffix}"
      templated_link = "#{url_template}#{sso_string}#{course_link_suffix}"

      csv << [row[6], link, templated_link]
    else
      csv << [row[6], "", ""]
    end
  end
puts "Generated #{output_filename}"

end
