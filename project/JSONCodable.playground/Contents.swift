//: Playground - noun: a place where people can play

import Cocoa

struct GroceryProduct: Codable {
  var name: String
  var points: Int
  var description: String?
}

let json = """
{
    "name": "Durian",
    "points": 600,
    "description": "A fruit with a distinctive scent."
}
""".data(using: .utf8)!
let decoder = JSONDecoder()
let product = try decoder.decode(GroceryProduct.self, from: json)
print("json: \(product.name)")

struct Ability: Codable {
  var mathematics: String
  var physics: String
  var chemistry: String
}
