import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from agents.orchestrators.request_type import parse_user_request
from agents.orchestrators.main_support import generate_final_response

router = APIRouter()

@router.websocket("/ws/query")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            user_input = json.loads(data).get("text")
            
            # Step 1: Routing [cite: 52]
            await websocket.send_json({"status": "🧠 Parsing intent...", "step": "routing"})
            structured_request = parse_user_request(user_input)
            
            # Step 2: Delegation & Synthesis [cite: 53, 57]
            await websocket.send_json({"status": "📊 Swarm activated (Market/News/Windsor)...", "step": "analyzing"})
            
            # Step 3: Risk Assessment & Delivery [cite: 58, 59]
            final_response = generate_final_response(user_input, structured_request)
            
            await websocket.send_json({
                "status": "Complete",
                "step": "done",
                "response": final_response
            })
    except WebSocketDisconnect:
        pass