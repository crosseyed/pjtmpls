// prj:render
package main

import (
    "fmt"
    "{{ .Env.GOSERVER }}/{{ .Env.GOGROUP }}/{{ .Project.NAME }}/internal/options"
    "os"
)

func main() {
    opts := options.GetUsage(os.Args[1:],internal.Version)
    _ = opts
}
