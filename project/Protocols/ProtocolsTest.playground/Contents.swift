//: Playground - noun: a place where people can play

import Cocoa

protocol Animalable {
  func eat() -> String
}

protocol Growable {
  var age: Int { get }
}

func printAgeOfAnimal(animal: Animalable & Growable) {
  print("\(animal.age), \(animal.eat())")
}

class Animal: Animalable, Growable {
  
  var age: Int {
    return 18
  }
  
  func eat() -> String {
    return "eat"
  }
  
}

printAgeOfAnimal(animal: Animal())


// Generic Protocol

protocol Storable {
  
  associatedtype Store
  
  init(_ value: Store)
  
  func getStore() -> Store
  
}

struct IntStore: Storable {
  
  typealias Store = Int
  
  private let _store: Int
  
  init(_ value: Store) {
    self._store = value
  }
  
  func getStore() -> Int {
    return _store
  }
  
}

struct StringStore: Storable {
  
  typealias Store = String
  
  private let _store: String
  
  init(_ value: Store) {
    self._store = value
  }
  
  func getStore() -> String {
    return _store
  }
  
}

let intStore = IntStore(5)
intStore.getStore()

let stringStore = StringStore("dyl")
stringStore.getStore()

// As you have seen this won't compile because Storable has associated type.

// error... protocol 'Storable' can only be used as a generic constraint because it has Self or associated type requirements
//var someStore: Storable = arc4random() % 2 == 0 ? intStore :  stringStore
//let x = someStore.getStore()

// In swift, all types must be fixed at compile time

func printStoreValue<S: Storable>(store: S) {
  let x = store.getStore()
  print("x: \(x)")
}

printStoreValue(store: intStore)
printStoreValue(store: stringStore)

