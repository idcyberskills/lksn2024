<?php
session_start();

$_SESSION["diamond_jackpot"] = 0;
header('Location: /slot.html');