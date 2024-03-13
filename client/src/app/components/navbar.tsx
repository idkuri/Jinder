
import Link from "next/link"
import "./styles/navbar.css"
export default function Navbar() {

    return(
        <div className="navbar">
            <div className="flex-1">
                <Link className="btn btn-ghost text-xl" href = "/">Jinder</Link>
            </div>
            <Link className="btn btn-ghost text-l" href = "/login">Login</Link>
            <Link className="btn btn-ghost text-l" href = "/register">Register</Link>
        </div>
    )
}
