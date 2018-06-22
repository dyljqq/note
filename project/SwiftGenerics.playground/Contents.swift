//: Playground - noun: a place where people can play

import Cocoa

//struct Buffer {
//
//  var count: Int
//
//  subscript(at: Int) -> Int {
//    get { return 1 }
//  }
//
//}
//
//struct StringBuffer {
//
//  var count: Int
//
//  subscript(at: Int) -> String {
//    get { return "1" }
//  }
//
//}

struct AnyBuffer {
  var array: [Any]
  
  var count: Int {
    get { return array.count }
  }
  
  init(array: [Any]) {
    self.array = array
  }
  
  subscript(_ index: Int) -> Any {
    get { return self.array[index] }
    set { self.array[index] = newValue }
  }
}

var words: AnyBuffer = AnyBuffer(array: ["12", "34", 56])
words[0] = 42
print(words)
