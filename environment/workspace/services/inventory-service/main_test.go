package main

import (
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"
)

func TestHealthHandler(t *testing.T) {
	req := httptest.NewRequest(http.MethodGet, "/health", nil)
	w := httptest.NewRecorder()

	healthHandler(w, req)

	if w.Code != http.StatusOK {
		t.Errorf("Expected status 200, got %d", w.Code)
	}

	var response map[string]string
	json.NewDecoder(w.Body).Decode(&response)

	if response["status"] != "healthy" {
		t.Errorf("Expected status 'healthy', got '%s'", response["status"])
	}

	if response["service"] != "inventory-service" {
		t.Errorf("Expected service 'inventory-service', got '%s'", response["service"])
	}
}

func TestGetInventoryHandler(t *testing.T) {
	inventory["test-1"] = Product{ID: "test-1", Name: "Test Product", Quantity: 10, Price: 19.99}
	
	req := httptest.NewRequest(http.MethodGet, "/api/v1/inventory", nil)
	w := httptest.NewRecorder()

	getInventoryHandler(w, req)

	if w.Code != http.StatusOK {
		t.Errorf("Expected status 200, got %d", w.Code)
	}

	var response map[string][]Product
	json.NewDecoder(w.Body).Decode(&response)

	products := response["products"]
	if len(products) == 0 {
		t.Error("Expected products in inventory, got empty list")
	}

	delete(inventory, "test-1")
}

func TestGetProductHandler_Success(t *testing.T) {
	inventory["test-2"] = Product{ID: "test-2", Name: "Widget", Quantity: 100, Price: 29.99}
	
	req := httptest.NewRequest(http.MethodGet, "/api/v1/inventory/test-2", nil)
	w := httptest.NewRecorder()

	getProductHandler(w, req)

	if w.Code != http.StatusOK {
		t.Errorf("Expected status 200, got %d", w.Code)
	}

	var product Product
	json.NewDecoder(w.Body).Decode(&product)

	if product.ID != "test-2" {
		t.Errorf("Expected product ID 'test-2', got '%s'", product.ID)
	}

	if product.Name != "Widget" {
		t.Errorf("Expected product name 'Widget', got '%s'", product.Name)
	}

	if product.Quantity != 100 {
		t.Errorf("Expected quantity 100, got %d", product.Quantity)
	}

	if product.Price != 29.99 {
		t.Errorf("Expected price 29.99, got %.2f", product.Price)
	}

	delete(inventory, "test-2")
}

func TestGetProductHandler_NotFound(t *testing.T) {
	req := httptest.NewRequest(http.MethodGet, "/api/v1/inventory/nonexistent", nil)
	w := httptest.NewRecorder()

	getProductHandler(w, req)

	if w.Code != http.StatusNotFound {
		t.Errorf("Expected status 404, got %d", w.Code)
	}

	var response map[string]string
	json.NewDecoder(w.Body).Decode(&response)

	if response["error"] != "Product not found" {
		t.Errorf("Expected error 'Product not found', got '%s'", response["error"])
	}
}

func TestGetInventoryHandler_EmptyInventory(t *testing.T) {
	originalInventory := make(map[string]Product)
	for k, v := range inventory {
		originalInventory[k] = v
	}
	inventory = make(map[string]Product)

	req := httptest.NewRequest(http.MethodGet, "/api/v1/inventory", nil)
	w := httptest.NewRecorder()

	getInventoryHandler(w, req)

	if w.Code != http.StatusOK {
		t.Errorf("Expected status 200, got %d", w.Code)
	}

	var response map[string][]Product
	json.NewDecoder(w.Body).Decode(&response)

	if len(response["products"]) != 0 {
		t.Errorf("Expected empty products list, got %d products", len(response["products"]))
	}

	inventory = originalInventory
}

func TestConcurrentAccess(t *testing.T) {
	inventory["concurrent-1"] = Product{ID: "concurrent-1", Name: "Concurrent Product", Quantity: 50, Price: 15.99}

	done := make(chan bool)

	for i := 0; i < 10; i++ {
		go func() {
			req := httptest.NewRequest(http.MethodGet, "/api/v1/inventory/concurrent-1", nil)
			w := httptest.NewRecorder()
			getProductHandler(w, req)
			
			if w.Code != http.StatusOK {
				t.Errorf("Expected status 200, got %d", w.Code)
			}
			done <- true
		}()
	}

	for i := 0; i < 10; i++ {
		<-done
	}

	delete(inventory, "concurrent-1")
}

func TestProductJSONSerialization(t *testing.T) {
	product := Product{
		ID:       "json-test",
		Name:     "JSON Product",
		Quantity: 25,
		Price:    99.99,
	}

	data, err := json.Marshal(product)
	if err != nil {
		t.Fatalf("Failed to marshal product: %v", err)
	}

	var decoded Product
	err = json.Unmarshal(data, &decoded)
	if err != nil {
		t.Fatalf("Failed to unmarshal product: %v", err)
	}

	if decoded.ID != product.ID {
		t.Errorf("Expected ID '%s', got '%s'", product.ID, decoded.ID)
	}

	if decoded.Name != product.Name {
		t.Errorf("Expected Name '%s', got '%s'", product.Name, decoded.Name)
	}

	if decoded.Quantity != product.Quantity {
		t.Errorf("Expected Quantity %d, got %d", product.Quantity, decoded.Quantity)
	}

	if decoded.Price != product.Price {
		t.Errorf("Expected Price %.2f, got %.2f", product.Price, decoded.Price)
	}
}