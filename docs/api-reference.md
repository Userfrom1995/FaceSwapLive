# API Reference

This document describes the Face Swap Live server API endpoints and WebSocket events.

## HTTP Endpoints

### GET /
**Description**: Main application interface
**Response**: HTML page with web interface

### POST /upload_source
**Description**: Upload source face image
**Content-Type**: `multipart/form-data`
**Parameters**:
- `image` (file): Image file containing source face

**Response**:
```json
{
  "success": true,
  "message": "Source face ready!"
}
```

**Error Response**:
```json
{
  "success": false,
  "message": "No face detected"
}
```

### GET /status
**Description**: Get server performance statistics
**Response**:
```json
{
  "frame_count": 1234,
  "swap_count": 1200,
  "error_count": 34,
  "avg_processing_time": 45.2,
  "source_face_loaded": true,
  "models_loaded": true
}
```

## WebSocket Events

### Client to Server Events

#### connect
**Description**: Client connects to server
**Behavior**: 
- Single user mode: disconnects previous user if present
- Sets client as current active user

#### process_frame
**Description**: Send frame for face swapping
**Data**:
```json
{
  "frame": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQ..."
}
```

**Requirements**:
- Frame must be base64-encoded image data
- Client must be the active user
- Source face must be uploaded first

#### clear_source
**Description**: Clear the uploaded source face
**Data**: None
**Behavior**: Removes stored source face from memory

#### disconnect
**Description**: Client disconnects from server
**Behavior**: Clears active user session

### Server to Client Events

#### processed_frame
**Description**: Returns processed frame with face swap
**Data**:
```json
{
  "success": true,
  "processed": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQ...",
  "stats": {
    "frame_count": 1234,
    "swap_count": 1200,
    "avg_processing_time": 45.2,
    "fps": 15.3
  }
}
```

**Error Response**:
```json
{
  "success": false,
  "error": "No face detected in frame",
  "processed": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQ..."
}
```

#### status_update
**Description**: Server status notifications
**Data**:
```json
{
  "message": "Source cleared"
}
```

## Rate Limiting

### Frame Processing
- Maximum 15 frames per second per user
- Frames exceeding limit are dropped
- No error response for dropped frames

### Session Management
- Session timeout: 300 seconds (5 minutes)
- Maximum idle time: 60 seconds
- Single user mode enforced

## Error Handling

### HTTP Errors
- **400 Bad Request**: Invalid request format
- **413 Payload Too Large**: File exceeds size limit (16MB)
- **500 Internal Server Error**: Server processing error

### WebSocket Errors
- Connection rejected if another user is active (single user mode)
- Processing errors returned in `processed_frame` event
- Automatic reconnection supported by client

## Security Considerations

### File Upload Validation
- Allowed extensions: `.jpg`, `.jpeg`, `.png`, `.bmp`, `.webp`
- Maximum file size: 10MB
- File content validation performed

### Access Control
- Single user mode prevents concurrent access
- Session-based user tracking
- Automatic cleanup of inactive sessions

### Rate Limiting
- Per-user frame rate limiting
- Session timeout enforcement
- Resource usage monitoring

## Performance Metrics

### Statistics Tracking
- Total frames processed
- Successful face swaps
- Processing errors
- Average processing time
- Real-time FPS calculation

### Monitoring
- Statistics updated every 30 frames
- Performance logs available in debug mode
- Resource usage tracking