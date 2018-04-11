//: Playground - noun: a place where people can play

import Cocoa

// For loop with Half-open range

// With Half-open range operator
let names = ["jqq", "dyl", "dyljqq"]
for name in names[0..<2] {
  print("name:\(name)")
}
for name in names[..<2] {
  print("name: \(name)")
}

// Without Half-open range operator
for (index, name) in names.enumerated() {
  if index < 2 {
    print("\(name)")
  }
}

var index = 0
while index < 2 {
  print("\(names[index])")
  index += 1
}


// Subscripts

// Without Subscripts
struct Matrix {
  let rows: Int
  let columns: Int
  var grid: [Double]
  
  init(rows: Int, columns: Int) {
    self.rows = rows
    self.columns = columns
    self.grid = Array(repeatElement(0.0, count: rows * columns))
  }
  
  func getValue(row: Int, column: Int) -> Double {
    return grid[(row * columns) + column]
  }
  
  mutating func setValue(row: Int, column: Int, value: Double) {
    grid[(row * columns) + column] = value
  }
}

var matrix = Matrix(rows: 2, columns: 2)
matrix.setValue(row: 0, column: 0, value: 1.0)
matrix.setValue(row: 0, column: 1, value: 2.0)
matrix.setValue(row: 1, column: 0, value: 3.0)
matrix.setValue(row: 1, column: 1, value: 4.0)

print(matrix.getValue(row: 0, column: 0)) //prints "1.0"
print(matrix.getValue(row: 0, column: 1)) //prints "2.0"
print(matrix.getValue(row: 1, column: 0)) //prints "3.0"
print(matrix.getValue(row: 1, column: 1)) //prints "4.0"

// With Subscrips

struct Matrix1 {
  let rows: Int
  let columns: Int
  var grid: [Double]
  
  init(rows: Int, columns: Int) {
    self.rows = rows
    self.columns = columns
    self.grid = Array(repeatElement(0.0, count: rows * columns))
  }
  
  subscript(row: Int, column: Int) -> Double {
    get {
      return grid[(row * columns) + column]
    }
    
    set {
      grid[(row * columns) + column] = newValue
    }
  }
}

var matrix1 = Matrix1(rows: 2, columns: 2)
matrix1[0,0] = 1.0
matrix1[0,1] = 2.0
matrix1[1,0] = 3.0
matrix1[1,1] = 4.0
print(matrix1[0,0]) //prints "1.0"
print(matrix1[0,1]) //prints "2.0"
print(matrix1[1,0]) //prints "3.0"
print(matrix1[1,1]) //prints "4.0"

// Functional Programming

let evenNumbers = (1...10).filter { $0 % 2 == 0 }
print(evenNumbers)

