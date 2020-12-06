package main

import (
	"context"
	"encoding/json"
	"log"
	"net/http"
	"os"
	"os/signal"
	"strconv"
	"syscall"
	"time"
)

func main() {
	srv := &http.Server{Addr: ":3334"}
	http.HandleFunc("/", gachaHandler)

	go func() {
		if err := srv.ListenAndServe(); err != nil {
			log.Printf("shutdown the server with error: %+v\n", err)
		}
	}()

	quit := make(chan os.Signal, 1)
	signal.Notify(quit, syscall.SIGTERM)
	log.Printf("SIGNAL %d received, then shutting down...\n", <-quit)

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()
	if err := srv.Shutdown(ctx); err != nil {
		log.Println("failed to shutdown: %+v", err)
		os.Exit(1)
	}
}

func gachaHandler(w http.ResponseWriter, r *http.Request) {
	seed := r.FormValue("seed")
	if len(seed) == 0 {
		seed = "1"
	}
	seedInt, err := strconv.Atoi(seed)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	// get current time(HHmmss)
	jst := time.FixedZone("Asia/Tokyo", 9*60*60)
	nowStr := time.Now().In(jst).Format("150405")
	log.Println(nowStr)
	nowInt, err := strconv.Atoi(nowStr)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	sm := (seedInt + nowInt) % 100000
	log.Println(sm)
	var flag map[string]string

	if sm == 1337 {
		flag = map[string]string{
			"flag": "taskctf{this_is_dummy_flag}",
		}
	} else {
		flag = map[string]string{
			"flag": "You might not have a luck...",
			"sum":  strconv.Itoa(sm),
		}
	}
	res, _ := json.Marshal(flag)
	w.WriteHeader(http.StatusOK)
	_, err = w.Write(res)
    if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
}