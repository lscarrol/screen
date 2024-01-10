import Foundation

print("Welcome to our List App!")
print("Please enter the topics you would like for your list, separated by commas.")

let input = readLine()
if let input = input {
  let topics = input.split(separator: ",")
  var list = [String]()
  
  for topic in topics {
      list.append(String(topic))
  }
  
  print("Your list contains the following topics: \(list)")
} else {
  print("No input received.")
}


import SwiftUI

struct TopicRow: View {
   var topic: String
   
   var body: some View {
       Text(topic)
           .font(.headline)
   }
}

struct TopicsListView: View {
   var topics: [String]
   
   var body: some View {
       NavigationView {
           List(topics, id: \.self) { topic in
               TopicRow(topic: topic)
           }
           .navigationTitle("Topics")
       }
   }
}