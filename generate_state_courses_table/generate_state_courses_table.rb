require 'csv'
require 'erb'

def parse_cell(string)
  if string == nil
    return ""
  else
    parsed_strings = []
    array_newline_split = string.split("\n")
    array_newline_split.each do |line|
      line.split(",").each do |item|
        parsed_strings << item
      end
    end
    return parsed_strings.join("<br/>")
  end
end

def getHeight(string)
  if string == nil
    return 1
  else
    parsed_strings = []
      array_newline_split = string.split("\n")
      array_newline_split.each do |line|
        line.split(",").each do |item|
          parsed_strings << item
        end
      end
    return parsed_strings.size
  end
end

def getMaxHeight(data)
  heights = []
  data.each do |row|
    heights << getHeight(row[3])
    heights << getHeight(row[7])
  end
  return heights.max()
end

def main()
  data = CSV.read(ARGV.first, headers:true)

  output_filename = '_generated_state-required-courses.component.html'

  File.open(output_filename, 'w') do |f|
    template_table = File.read("state_table_template_table.html.erb")
    @courses = []
    @height = getMaxHeight(data)*20

    data.each do |row|
      #0 Verified, 1 Types, 2 State, 3 Task, 4 Topic,
      #5 Title, 6 SKU, 7 Credits, 8 Price, 9 Expiration, 10 Link

      @verified = row[0]
      @types= row[1]
      @state = row[2]
      @topics = parse_cell(row[4])
      @title = row[5]
      @link = row[10]
      @credits = parse_cell(row[7])
      @price = row[8]

      if (@state != nil)
        template_row = File.read("state_table_template_row.html.erb")
        @courses << ERB.new(template_row).result(binding)
      else
      #Currently we just use a blank row to determine if we should add a separator or not
      #Otherwise, we could further simplify and check if the state has changed
        template_separator = File.read("state_table_template_separator.html.erb")
        @courses << ERB.new(template_separator).result(binding)
      end
    end

    result = ERB.new(template_table).result(binding)
    f.write result
    puts "Generated #{output_filename}"
  end
end

main()
