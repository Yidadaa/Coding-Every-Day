import React, { useEffect, useRef, useState } from "react";
import {
  bufferTime,
  debounce,
  debounceTime,
  filter,
  fromEvent,
  interval,
  Observable,
  of,
  Subject,
  Subscriber,
  takeLast,
  throttle,
} from "rxjs";
import "./App.css";

type Todo = {
  content: string;
  done: boolean;
};

function App() {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [todo, setTodo] = useState("");

  const input$ = new Subject<string>();

  useEffect(() => {
    setTodos(
      new Array(2).fill(0).map((v, i) => ({
        content: "todo " + i.toString(),
        done: i % 2 === 0,
      }))
    );
  }, []);

  input$.pipe(filter((v) => v.length > 0)).subscribe((s) => {
    setTodo(s);
    console.log("subscribe", s);
  });

  const onInputChange = (s: string) => {
    input$.next(s);
    console.log("input", s);
  };

  const onTodoToggle = (index: number) => {
    const newTodos = todos.map((v, i) => ({
      ...v,
      done: i === index ? !v.done : v.done,
    }));
    setTodos(newTodos);
  };

  const onTodoBtn = () => {
    setTodos(
      [
        {
          content: todo,
          done: false,
        },
      ].concat(todos)
    );
    setTodo("");
  };

  return (
    <div className="app">
      <div className="app-content">
        <div className="app-header">TODO</div>
        <div className="todo-add">
          <input
            type="text"
            className="todo-input"
            value={todo}
            onChange={(e) => onInputChange(e.target.value)}
          />
          <button className="todo-btn" onClick={() => onTodoBtn()}>
            Add
          </button>
        </div>
        <div className="todo-list">
          {todos.map(({ content, done }, i) => {
            return (
              <div
                className={`todo-item ${done && "todo-item-checked"}`}
                key={i}
              >
                <input
                  type="checkbox"
                  className="todo-checkbox"
                  onChange={() => onTodoToggle(i)}
                  checked={done}
                />
                <div className="todo-content">
                  {done ? <del>{content}</del> : content}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}

export default App;
