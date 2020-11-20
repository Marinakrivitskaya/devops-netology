> **3.1.	Задача 3. Написание кода.**
> Цель этого задания закрепить знания о базовом синтаксисе языка. Можно использовать редактор кода на своем компьютере, либо использовать песочницу: https://play.golang.org/.
>
> 1. Напишите программу для перевода метров в футы (1 фут = 0.3048 метр). Можно запросить исходные данные у пользователя, а можно статически задать в коде. Для взаимодействия с пользователем можно использовать функцию Scanf:
> 1.	package main
> 2.	
> 3.	import "fmt"
> 4.	
> 5.	func main() {
> 6.	    fmt.Print("Enter a number: ")
> 7.	    var input float64
> 8.	    fmt.Scanf("%f", &input)
> 9.	
> 10.	    output := input * 2
> 11.	
> 12.	    fmt.Println(output)    
> 13.	}



**main.go**

```Goland
package main

import (
   "fmt"
   "math"
)

func main() {
   fmt.Print("Enter the number of meters: ")
   var input float64
   fmt.Scanf("%f", &input)
   meters2feet(input)


}

func meters2feet(meter float64) float64 {
   output := Round(meter / 0.3048)
   fmt.Println(meter, "meters = ", output, "feet")
   return output
}


// Round возвращает ближайшее целочисленное значение.
func Round(x float64) float64 {
   t := math.Trunc(x)
   if math.Abs(x-t) >= 0.5 {
      return t + math.Copysign(1, x)
   }
   return t
}
```



**main_test.go**

```Goland
package main
import (
   "testing"
)

//Изначально не работало как на лекции
//Решение https://forum.golangbridge.org/t/go-test-results-in-testing-warning-no-tests-to-run/13446
//put yours methods in capital letter TestFourPlusFour()
func TestMain(t *testing.T) {
   var v float64
   var x float64 = 1000
   v = meters2feet(x)
   if v != 3281 {
      t.Error("Expected 3281, got ", v)
   }


   var y float64 = 420
   v = meters2feet(y)
   if v != 1378 {
      t.Error("Expected 1378, got ", v)
   }
}
```





> 2. **Напишите программу, которая найдет наименьший элемент в любом заданном списке, например:**
>
> **x := []int{48,96,86,68,57,82,63,70,37,34,83,27,19,97,9,17,}**



**main.go**

```Goland
package main

import (
   "fmt"
)

func main() {
   // Задаем список и заполняем его
   x := []int{48,96,86,68,57,82,63,70,37,34,83,27,19,97,9,17,}
   findsmall(x)
}


func findsmall(x [] int) int {
   smallest := x[0]

   for _, val := range x {
      if val < smallest {
         smallest = val
      }
      //fmt.Printf("Value: %d\n", val)
   }
   fmt.Println("Smallest number= ", smallest)
   return smallest
}
```



**main_test.go**

```Goland
package main
import (
   "testing"
)


func TestMain(t *testing.T) {
   var v int
   x := []int{48, 96, 86, 68, 57, 82, 63, 70, 37, 34, 83, 27, 19, 97, 9, 17,}
   v = findsmall(x)
   if v != 9 {
      t.Error("Expected 9, got ", v)
   }


   y := []int{48, 96, 86, 68, 57, 82, 63, 70, 37, 34, 83, 27, 19, 97, 11, 17,}
   v = findsmall(y)
   if v != 11 {
      t.Error("Expected 9, got ", v)
   }
}
```

 

> 3. **Напишите программу, которая выводит числа от 1 до 100, которые делятся на 3. То есть (3, 6, 9, …).**
>
> **В виде решения ссылку на код или сам код.**



**main.go**

```Goland
package main

import "fmt"

func main() {
   div3()
}

func div3() []int {
   //срез для хранения результата работы функции
   var result []int /* срез неопределённого размера */

   for i := 1; i <= 100; i++ {
      //Деление по модулю
      if i % 3 == 0 {
         result = append(result,i)
         fmt.Printf("Value: %d\n", i)
      }
   }
   return result
}
```



**main_test.go**

```Goland
package main
import (
   "testing"
)


func TestMain(t *testing.T) {
   x := []int{3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45, 48, 51, 54, 57, 60, 63, 66, 69, 72, 75, 78, 81, 84, 87, 90, 93, 96, 99,}
   y := div3()

   for index, val := range x {
      if val != y[index] {
         t.Error("Expected val, got ", y[index])
      }
   }
}
```





