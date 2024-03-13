
import Link from "next/link"
export default function Navbar() {

    return(
        <div className="navbar bg-base-100">
            <div className="flex-1">
                <Link className="btn btn-ghost text-xl" href = "/">Jinder</Link>
            </div>
            <Link className="btn btn-ghost text-l" href = "/login">Login</Link>
            <Link className="btn btn-ghost text-l" href = "/register">Register</Link>
        </div>
    )
}
