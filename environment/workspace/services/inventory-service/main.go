// Inventory Service - Manages product inventory
package main

import (
	"encoding/json"
	"log"
	"net/http"
	"os"
	"sync"
)

type Product struct {
	ID       string `json:"id"`
	Name     string `json:"name"`
	Quantity int    `json:"quantity"`
	Price    float64 `json:"price"`
}

var (
	inventory = make(map[string]Product)
	mu        sync.RWMutex
)

func healthHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(map[string]string{
		"status":  "healthy",
		"service": "inventory-service",
	})
}

func getInventoryHandler(w http.ResponseWriter, r *http.Request) {
	mu.RLock()
	defer mu.RUnlock()
	
	products := make([]Product, 0, len(inventory))
	for _, p := range inventory {
		products = append(products, p)
	}
	
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(map[string]interface{}{
		"products": products,
	})
}

func getProductHandler(w http.ResponseWriter, r *http.Request) {
	productID := r.URL.Path[len("/api/v1/inventory/"):]
	
	mu.RLock()
	product, exists := inventory[productID]
	mu.RUnlock()
	
	w.Header().Set("Content-Type", "application/json")
	if exists {
		json.NewEncoder(w).Encode(product)
	} else {
		w.WriteHeader(http.StatusNotFound)
		json.NewEncoder(w).Encode(map[string]string{"error": "Product not found"})
	}
}

func main() {
	// Initialize sample inventory
	inventory["prod-1"] = Product{ID: "prod-1", Name: "Widget", Quantity: 100, Price: 29.99}
	inventory["prod-2"] = Product{ID: "prod-2", Name: "Gadget", Quantity: 50, Price: 49.99}
	
	http.HandleFunc("/health", healthHandler)
	http.HandleFunc("/api/v1/inventory", getInventoryHandler)
	http.HandleFunc("/api/v1/inventory/", getProductHandler)
	
	port := os.Getenv("PORT")
	if port == "" {
		port = "4000"
	}
	
	log.Printf("Inventory service listening on port %s", port)
	log.Fatal(http.ListenAndServe(":"+port, nil))
}