//: Playground - noun: a place where people can play

import Cocoa

let nations = ["Chinese", "American"]
func showNations() {
  
  // 1
  nations.map { nation in
    print("nation: \(nation)")
  }
  
  // 2
  nations.map { print("nation: \($0)") }
}

// Generic Type
func showArray<T>(_ arr: [T]) {
  arr.map { print("arr: \($0)") }
}

showArray(nations)

// 类型约束

struct HTNTransition<S: Hashable, E: Hashable> {
  
  let event: E
  let fromState: S
  let toState: S
  
  init(event: E, fromState: S, toState: S) {
    self.event = event
    self.fromState = fromState
    self.toState = toState
  }
  
}

// 关联类型

protocol HTNState {
  
  associatedtype StateType
  func add(_ item: StateType)
  
}

// 非泛型

struct State: HTNState {
  
  func add(_ item: Int) {
    // TODO
  }
  
}

// 泛型

struct StateG<T>: HTNState {
  
  func add(_ item: T) {
    // TODO
    print("add: \(item)")
  }
  
}

// 类型擦除

class StateDelegate<T> {
  var state: T
  // error: protocol 'HTNState' can only be used as a generic constraint because it has Self or associated type requirements
//  var delegate: HTNState
  var delegate: AnyErase<T>?
  
  init(state: T) {
    self.state = state
  }
  
  func doSomeThing() {
    delegate?.add(state)
  }
}

struct AnyErase<T>: HTNState {
  
  private var _foo: (T) -> ()
  
  init<Inject: HTNState>(_ obj: Inject) where Inject.StateType == T  {
    self._foo = obj.add
  }
  
  func add(_ item: T) {
    self._foo(item)
  }
}

let erase = StateDelegate(state: 100)
erase.delegate = AnyErase(StateG<Int>())
erase.doSomeThing()

// where 语句
func stateFilter<FromState: HTNState, ToState: HTNState>(_ fromState: FromState, _ toState: ToState) where FromState.StateType == ToState.StateType {
  // TODO
}

// 泛型和Any

func add<T>(_ input: T) -> T {
  // ...
  return input
}

func anyAdd(_ input: Any) -> Any {
  // ...
  // 你无法保证输入和输出的类型是相同的
  return input
}


