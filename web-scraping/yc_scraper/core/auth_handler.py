"""Authentication and cookie handling for Y Combinator job board."""

import os
from typing import Dict, Optional, List
import logging

logger = logging.getLogger(__name__)


class AuthHandler:
    """Handles authentication and cookies for Y Combinator job board access."""
    
    def __init__(self, session_cookie: Optional[str] = None):
        """Initialize auth handler.
        
        Args:
            session_cookie: Y Combinator session cookie. If None, uses YC_SESSION_COOKIE env var.
        """
        self.session_cookie = session_cookie or os.getenv("YC_SESSION_COOKIE")
        
        # Default user agents for rotation
        self.user_agents = [
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15"
        ]
        self.current_user_agent_index = 0
    
    def get_cookies(self) -> Dict[str, str]:
        """Get cookies for authentication.
        
        Returns:
            Dictionary of cookies to use for requests
        """
        cookies = {}
        
        if self.session_cookie:
            # The exact cookie name may vary - common YC cookie names include:
            # - _yc_session
            # - waas_session  
            # - session_id
            # You may need to inspect browser dev tools to get the exact cookie name
            cookies["_yc_session"] = self.session_cookie
            logger.info("Using session cookie for authentication")
        else:
            logger.warning("No session cookie provided - access may be limited to public content")
        
        return cookies
    
    def get_headers(self) -> Dict[str, str]:
        """Get headers for requests including user-agent.
        
        Returns:
            Dictionary of headers to use for requests
        """
        headers = {
            "User-Agent": self.get_user_agent(),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Cache-Control": "max-age=0"
        }
        
        return headers
    
    def get_user_agent(self) -> str:
        """Get current user agent (with rotation).
        
        Returns:
            User agent string
        """
        user_agent = self.user_agents[self.current_user_agent_index]
        self.current_user_agent_index = (self.current_user_agent_index + 1) % len(self.user_agents)
        return user_agent
    
    def set_session_cookie(self, cookie: str) -> None:
        """Set session cookie for authentication.
        
        Args:
            cookie: Session cookie value
        """
        self.session_cookie = cookie
        logger.info("Session cookie updated")
    
    def is_authenticated(self) -> bool:
        """Check if authentication credentials are available.
        
        Returns:
            True if session cookie is available
        """
        return self.session_cookie is not None
    
    def get_cookie_instructions(self) -> str:
        """Get instructions for obtaining the session cookie.
        
        Returns:
            Instructions for getting the cookie from browser
        """
        return """
        To get your Y Combinator session cookie:
        
        1. Open your browser and go to https://www.workatastartup.com/
        2. Log in to your Y Combinator account
        3. Open browser Developer Tools (F12 or right-click -> Inspect)
        4. Go to the "Application" or "Storage" tab
        5. Under "Cookies", find the domain "workatastartup.com"
        6. Look for cookies named like "_yc_session", "waas_session", or similar
        7. Copy the cookie value (the long string after the "=")
        8. Set it in your .env file as YC_SESSION_COOKIE=<cookie_value>
        
        Note: This cookie will expire periodically and you'll need to update it.
        """