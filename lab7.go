package main

import (
	"fmt"
	"net"
	"os"
	"strings"
	"time"
)

func listen_and_writeToConsole() {
	laddr := net.UDPAddr{
		IP:   nil,
		Port: 8080,
	}
	socket, _ := net.ListenUDP("udp", &laddr)
	for {
		p := make([]byte, 1024)
		_, from, _ := socket.ReadFromUDP(p)
		fmt.Printf("From: %v, message: %s", from, p)
	}
}

// to send message
func main() {
	go listen_and_writeToConsole()
	for {
		var name string
		var msg string
		fmt.Print("\nReciver: ")
		fmt.Fscan(os.Stdin, &name)
		if strings.Compare(name, "all") == 0 {
			fmt.Print("Message for all: ")
			fmt.Fscan(os.Stdin, &msg)
			raddr := net.UDPAddr{
				IP:   net.IPv4(255, 255, 255, 255),
				Port: 8080,
			}
			conn, _ := net.DialUDP("udp", nil, &raddr)
			message := []byte(msg)
			_, _ = conn.Write(message)
			time.Sleep(1 * time.Second)
		} else {
			fmt.Print("Message for ", name, ": ")
			fmt.Fscan(os.Stdin, &msg)
			raddr := net.UDPAddr{
				IP:   net.ParseIP(name),
				Port: 8080,
			}
			conn, err := net.DialUDP("udp", nil, &raddr)
			if err != nil {
				panic(err)
			}
			message := []byte(msg)
			_, _ = conn.Write(message)
			time.Sleep(1 * time.Second)
		}
	}
}
