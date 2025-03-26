from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# In-memory list to store items
items = [
    {"id": 1, "name": "Item 1", "description": "First item"},
    {"id": 2, "name": "Item 2", "description": "Second item"},
]

# GET /api/items/ → Return all items
def get_items(request):
    search_query = request.GET.get("search", "")
    if search_query:
        filtered_items = [item for item in items if search_query.lower() in item["name"].lower()]
        return JsonResponse(filtered_items, safe=False)
    return JsonResponse(items, safe=False)

# GET /api/items/<int:item_id>/ → Get a single item
def get_item(request, item_id):
    item = next((item for item in items if item["id"] == item_id), None)
    if item:
        return JsonResponse(item, safe=False)
    return JsonResponse({"error": "Item not found"}, status=404)

# POST /api/items/add/ → Add a new item
@csrf_exempt
def add_item(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            new_item = {
                "id": len(items) + 1,
                "name": data["name"],
                "description": data.get("description", ""),
            }
            items.append(new_item)
            return JsonResponse(new_item, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

# PUT /api/items/update/<int:item_id>/ → Update an item
@csrf_exempt
def update_item(request, item_id):
    if request.method == "PUT":
        try:
            data = json.loads(request.body)
            for item in items:
                if item["id"] == item_id:
                    item["name"] = data.get("name", item["name"])
                    item["description"] = data.get("description", item["description"])
                    return JsonResponse(item)
            return JsonResponse({"error": "Item not found"}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

# DELETE /api/items/delete/<int:item_id>/ → Delete an item
@csrf_exempt
def delete_item(request, item_id):
    global items
    items = [item for item in items if item["id"] != item_id]
    return JsonResponse({"message": "Item deleted"}, status=200)
