import React from 'react';
import Link from 'next/link';

const Header: React.FC = () => {
  return (
    <header className="bg-gray-200 py-4">
      <div className="container mx-auto text-center">
        <nav className="space-x-8">
          <Link href="/" className="text-lg text-blue-600 hover:text-blue-800">
            Home
          </Link>
          <Link href="/select-images" className="text-lg text-blue-600 hover:text-blue-800">
            picture chooser
          </Link>
        </nav>
      </div>
    </header>
  );
};

export default Header;
