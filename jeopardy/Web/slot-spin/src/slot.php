<?php
session_start();
if (!isset($_SESSION['diamond_jackpot'])) $_SESSION["diamond_jackpot"] = 0;

// Receive and decode the JSON data
$json = file_get_contents('php://input');
$data = json_decode($json, true);

if ($data["reels"][0] == 100 && $data["reels"][1] == 100 && $data["reels"][2] == 100) {
    $_SESSION["diamond_jackpot"] = $_SESSION["diamond_jackpot"]+1;
}

$response = [
    'status' => 'success',
    'message' => 'Spin data received',
    'data' => $_SESSION["diamond_jackpot"]
];

if ($_SESSION["diamond_jackpot"] >= 10) {
    $response['flag'] = getenv('FLAG');
} 

// Send JSON response
header('Content-Type: application/json');
echo json_encode($response);